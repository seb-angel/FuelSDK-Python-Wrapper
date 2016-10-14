# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import FuelSDK
import time
from FuelSDK.rest import ET_Constructor
from datetime import date, datetime

logger_debug = logging.getLogger('FuelSDK-Wrapper')


class Operator:

    EQUALS = 'equals'
    NOT_EQUALS = 'notEquals'
    GREATER_THAN = 'greaterThan'
    LESS_THAN = 'lessThan'


class ObjectType:

    CAMPAIGN = 'ET_Campaign'
    CAMPAIGN_ASSET = 'ET_Campaign_Asset'
    CONTENT_AREA = 'ET_ContentArea'
    DATA_EXTENSION = 'ET_DataExtension'
    DATA_EXTENSION_ROW = 'ET_DataExtension_Row'
    EMAIL = 'ET_Email'
    FOLDER = 'ET_Folder'
    LIST = 'ET_List'
    PROFILE_ATTRIBUTE = 'ET_ProfileAttribute'
    SUBSCRIBER = 'ET_Subscriber'
    TRIGGERED_SEND = 'ET_TriggeredSend'

    # Events
    BOUNCE_EVENT = 'ET_BounceEvent'
    CLICK_EVENT = 'ET_ClickEvent'
    OPEN_EVENT = 'ET_OpenEvent'
    SENT_EVENT = 'ET_SentEvent'
    UNSUB_EVENT = 'ET_UnsubEvent'

    # Non FuelSDK
    SEND = 'Send'
    IMPORT_DEFINITION = 'ImportDefinition'
    IMPORT_RESULTS_SUMMARY = 'ImportResultsSummary'


def validate_response():
    def dec(func):
        def wrapper(*args, **kwargs):
            start = time.clock()
            response = func(*args, **kwargs)
            end = time.clock()
            logger_debug.debug('API Execution Time: {0} - {1} results'.format(humanize_time(end - start), len(response.results)))
            ET_API.check_response(response)
            return response
        return wrapper
    return dec


def humanize_time(secs):
    if type(secs) == str:
        secs = float(secs)
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return '%d:%02d:%02d' % (hours, mins, secs)


class ET_Object(FuelSDK.ET_CUDSupport):
    def __init__(self, object_type):
        super(ET_Object, self).__init__()
        self.obj_type = object_type


class ET_ObjectRest(FuelSDK.ET_CUDSupportRest):
    def __init__(self, object_type):
        super(ET_ObjectRest, self).__init__()
        self.endpoint = 'https://www.exacttargetapis.com/hub/v1/{}/{}'.format(object_type.lower(), '{id}')
        self.urlProps = ["id"]
        self.urlPropsRequired = []


class ET_Perform(ET_Constructor):
    def __init__(self, auth_stub, action, object_source=None):
        auth_stub.refresh_token()

        ws_performRequest = auth_stub.soap_client.factory.create('PerformRequestMsg')
        ws_performRequest.Options = auth_stub.soap_client.factory.create('Options')
        ws_performRequest.Action = action

        ws_definition = auth_stub.soap_client.factory.create(type(object_source).__name__)
        ws_definition.CustomerKey = object_source.CustomerKey
        ws_performRequest.Definitions = [ws_definition]

        response = auth_stub.soap_client.service.Perform(ws_performRequest)

        if response is not None:
            super(ET_Perform, self).__init__(response)


class ET_API:

    client = None

    def __init__(self, get_server_wsdl=False, debug=False, params=None):
        # Set Debug to True for more information
        if debug:
            logger_debug.setLevel(logging.DEBUG)

        self.client = FuelSDK.ET_Client(get_server_wsdl=get_server_wsdl, debug=debug, params=params)

    class SalesforceApiError(Exception):
        pass

    class ObjectAlreadyExists(Exception):
        pass

    class ObjectDoesntExist(Exception):
        pass

    @staticmethod
    def check_response(response):
        if response.message and response.message not in ('OK', 'MoreDataAvailable'):
            if len(response.results) > 0 and 'already in use' in response.results[0].StatusMessage:
                raise ET_API.ObjectAlreadyExists('Object already exists')
            elif len(response.results) > 0 and 'Concurrency violation' in response.results[0].ErrorMessage:
                raise ET_API.ObjectDoesntExist("Object doesn't exist")
            elif len(response.results) > 0:
                raise ET_API.SalesforceApiError('Error: {}'.format(response.results[0].StatusMessage))
            else:
                raise ET_API.SalesforceApiError('{}'.format(response.message))

        logger_debug.debug('Post Status: {}; Code: {}; Message: {}; Result Count: {}'
                           .format(response.status, response.code, response.message, len(response.results)))

    def get_client(self):
        if not self.client:
            self.__init__()
        return self.client

    def parse_object(self, object_type, properties):
        return FuelSDK.rest.ET_Constructor().parse_props_into_ws_object(self.get_client(), object_type, properties)

    @staticmethod
    def search_filter(property_name, operator, value):
        value_type = 'Value'
        if isinstance(value, date) or isinstance(value, datetime):
            value_type = 'DateValue'

        return {
            'Property': property_name,
            'SimpleOperator': operator,
            value_type: value
        }

    def get_object_class(self, object_type, is_rest=False):
        try:
            if object_type.startswith('ET_'):
                obj = getattr(FuelSDK, object_type)()
            else:
                obj = getattr(FuelSDK, 'ET_{}'.format(object_type))()
        except AttributeError:
            if is_rest:
                obj = globals()['ET_ObjectRest'](object_type)
            else:
                obj = globals()['ET_Object'](object_type)

        obj.auth_stub = self.get_client()
        return obj

    def get_info(self, object_type):
        obj = self.get_object_class(object_type)
        try:
            return obj.info().results[0].Properties
        except IndexError:
            return []

    def perform_action(self, action, object_source=None):
        auth_stub = self.get_client()
        res = ET_Perform(auth_stub, action, object_source)
        return res

    @validate_response()
    def get_objects(self, object_type, search_filter=None, property_list=None, is_rest=False, is_global=False):
        obj = self.get_object_class(object_type, is_rest)
        if search_filter:
            obj.search_filter = search_filter
        if property_list:
            obj.props = property_list
        if is_global:
            obj.QueryAllAccounts = True
        return obj.get()

    @validate_response()
    def continue_request(self, request_id):
        auth_stub = self.get_client()
        obj = FuelSDK.rest.ET_Continue(auth_stub, request_id)
        return obj

    @validate_response()
    def create_object(self, object_type, property_dict, data_extension_key=None, is_rest=False):
        obj = self.get_object_class(object_type, is_rest)
        if object_type == ObjectType.DATA_EXTENSION_ROW:
            obj.CustomerKey = data_extension_key
        obj.props = property_dict
        return obj.post()

    @validate_response()
    def update_object(self, object_type, object_id_dict, values_dict, data_extension_key=None, is_rest=False):
        obj = self.get_object_class(object_type, is_rest)
        if object_type == ObjectType.DATA_EXTENSION_ROW:
            obj.CustomerKey = data_extension_key
            obj.props = values_dict
        else:
            obj.props = object_id_dict
            obj.props.update(values_dict)
        return obj.patch()

    @validate_response()
    def delete_object(self, object_type, object_id, is_rest=False):
        obj = self.get_object_class(object_type, is_rest)
        obj.props = {'ID': object_id}
        return obj.delete()

    # Specific methods
    def get_data_extension_columns(self, customer_key, property_list=None):
        search_filter = self.search_filter('DataExtension.CustomerKey', Operator.EQUALS, customer_key)
        return self.get_objects('ET_DataExtension_Column', search_filter, property_list)

    def get_list_subscriber(self, search_filter=None, property_list=None):
        return self.get_objects('ET_List_Subscriber', search_filter, property_list)

    def get_data_extension_rows(self, customer_key, search_filter=None, property_list=None):
        de_row = FuelSDK.ET_DataExtension_Row()
        de_row.auth_stub = self.get_client()
        de_row.CustomerKey = customer_key
        if search_filter:
            de_row.search_filter = search_filter
        if property_list:
            de_row.props = property_list
        return de_row.get()

    # Convenience methods
    @validate_response()
    def add_subscriber_to_list(self, email, list_ids, subscriber_key=None):
        return self.get_client().AddSubscriberToList(email, list_ids, subscriber_key)

    @validate_response()
    def create_data_extension(self, name, columns, customer_key=None):
        data_extension = {
            'Name': name,
            'CustomerKey': customer_key,
            'columns': columns
        }
        response = self.get_client().CreateDataExtensions([data_extension])
        return response

    def create_campaign(self, name, description, campaign_code, color='Public', is_favorite=False):
        if color not in ('Public', 'Private'):
            raise self.SalesforceApiError('Invalid color, must be: Public or Private')

        property_dict = {
            'name': name,
            'description': description,
            'campaignCode': campaign_code,
            'color': color,
            'favorite': is_favorite
        }
        return self.create_object(ObjectType.CAMPAIGN, property_dict)

    def create_html_paste_email(self, customer_key, category_id, name, subject, pre_header, html, plain_text):
        property_dict = {
            'CustomerKey': customer_key,
            'CategoryID': category_id,
            'Name': name,
            'Subject': subject,
            'PreHeader': pre_header,
            'HTMLBody': html,
            'TextBody': plain_text,
            'EmailType': 'HTML',
            'CharacterSet': 'UTF-8',
            'IsHTMLPaste': True
        }
        try:
            return self.create_object(ObjectType.EMAIL, property_dict)
        except self.ObjectAlreadyExists:
            object_id_dict = {'CustomerKey': customer_key}
            return self.update_object(ObjectType.EMAIL, object_id_dict, property_dict)

    def create_subscriber(self, attributes):
        self.create_object(ObjectType.DATA_EXTENSION_ROW, attributes,
                           data_extension_key='subscribers_dataextension')

    def update_subscriber(self, object_id, attributes):
        object_id_dict = {'ID': object_id}
        self.update_object(ObjectType.DATA_EXTENSION_ROW, object_id_dict, attributes,
                           data_extension_key='subscribers_dataextension')

    def get_or_update_user_initiated_email(self, subscription_name, email_name):
        res = self.get_objects(
            'EmailSendDefinition',
            self.search_filter('Name', Operator.EQUALS, subscription_name),
            ['Email.ID']
        )
        try:
            email_id = res.results[-1].Email.ID
            res = self.get_objects(ObjectType.EMAIL, self.search_filter('ID', Operator.EQUALS, email_id), ['Name'])
            if res.results[-1].Name == email_name:
                return subscription_name
        except IndexError:
            pass

        object_id_dict = {'CustomerKey': subscription_name}
        self.update_object('EmailSendDefinition', object_id_dict, {
            'Email': {
                'CustomerKey': email_name
            }
        })
        return subscription_name

    def send_email(self, user_initiated_key, start_datetime):
        recurrence = self.parse_object('DailyRecurrence', {
            'DailyRecurrencePatternType': 'Interval',
            'DayInterval': 1
        })

        schedule = self.parse_object('ScheduleDefinition', {
            'Occurrences': 1,
            'StartDateTime': start_datetime,
            'RecurrenceType': 'Daily',
            'RecurrenceRangeType': 'EndAfter',
            'Recurrence': recurrence
        })

        email_send = self.parse_object('EmailSendDefinition', {
            'CustomerKey': user_initiated_key
        })

        return self.get_client().soap_client.service.Schedule(None, 'start', schedule, [{'Interaction': email_send}])
