# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import suds
import time
import logging
import FuelSDK
import requests
from datetime import date, datetime

logger_debug = logging.getLogger('FuelSDKWrapper')


class Operator:

    EQUALS = 'equals'
    NOT_EQUALS = 'notEquals'
    IS_NULL = 'isNull'
    IS_NOT_NULL = 'isNotNull'
    GREATER_THAN = 'greaterThan'
    GREATER_THAN_OR_EQUAL = 'greaterThanOrEqual'
    LESS_THAN = 'lessThan'
    LESS_THAN_OR_EQUAL = 'lessThanOrEqual'
    BETWEEN = 'between'
    LIKE = 'like'
    IN = 'IN'


class ObjectType:

    CAMPAIGN = 'ET_Campaign'
    CAMPAIGN_ASSET = 'ET_Campaign_Asset'
    CONTENT_AREA = 'ET_ContentArea'
    DATA_EXTENSION = 'ET_DataExtension'
    DATA_EXTENSION_COLUMN = 'ET_DataExtension_Column'
    DATA_EXTENSION_ROW = 'ET_DataExtension_Row'
    EMAIL = 'ET_Email'
    FOLDER = 'ET_Folder'
    LIST = 'ET_List'
    LIST_SUBSCRIBER = 'ET_List_Subscriber'
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
    AUTOMATION = 'Automation'
    IMPORT_DEFINITION = 'ImportDefinition'
    IMPORT_RESULTS_SUMMARY = 'ImportResultsSummary'
    PORTFOLIO = 'Portfolio'
    QUERY_DEFINITION = 'QueryDefinition'
    SEND = 'Send'
    TEMPLATE = 'Template'
    ACCOUNT = 'Account'
    ACCOUNT_USER = 'AccountUser'
    BRAND = 'Brand'
    BRAND_TAG = 'BrandTag'
    BUSINESS_UNIT = 'BusinessUnit',
    DATA_EXTENSION_TEMPLATE = 'DataExtensionTemplate'
    DOUBLE_OPTIN_MO_KEYWORD = 'DoubleOptInMOKeyword'
    EMAIL_SEND_DEFINITION = 'EmailSendDefinition'
    FILE_TRIGGER = 'FileTrigger'
    FILE_TRIGGER_TYPE_LAST_PULL = 'FileTriggerTypeLastPull'
    FILTER_DEFINITION = 'FilterDefinition'
    FORWARDED_EMAIL_EVENT = 'ForwardedEmailEvent'
    FORWARDED_EMAIL_OPTIN_EVENT = 'ForwardedEmailOptInEvent'
    GROUP = 'Group'
    HELP_MO_KEYWORD = 'HelpMOKeyword'
    HIVE_QUERY_DEFINITION = 'HiveQueryDefinition'
    LINK_SEND = 'LinkSend'
    LIST_ATTRIBUTE = 'ListAttribute'
    LIST_SEND = 'ListSend'
    MESSAGE_VENDOR_KIND = 'MessagingVendorKind'
    NOT_SEND_EVENT = 'NotSentEvent'
    PLATFORM_APPLICATION = 'PlatformApplication'
    PLATFORM_APPLICATION_PACKAGE = 'PlatformApplicationPackage'
    PRIVATE_IP = 'PrivateIP'
    PROGRAM_MANIFEST_TEMPLATE = 'ProgramManifestTemplate'
    PUBLIC_KEY_MANAGEMENT = 'PublicKeyManagement'
    PUBLICATION = 'Publication'
    PUBLICATION_SUBSCRIBER = 'PublicationSubscriber'
    REPLY_MAIL_MANAGEMENT_CONFIGURATION = 'ReplyMailManagementConfiguration'
    RESULT_ITEM = 'ResultItem'
    RESULT_MESSAGE = 'ResultMessage'
    ROLE = 'Role'
    SMS_MO_EVENT = 'SMSMOEvent'
    SMS_MT_EVENT = 'SMSMTEvent'
    SMS_SHARED_KEYWORD = 'SMSSharedKeyword'
    SMS_TRIGGERED_SEND = 'SMSTriggeredSend'
    SMS_TRIGGERED_SEND_DEFINITION = 'SMSTriggeredSendDefinition'
    SEND_ADDITIONAL_ATTRIBUTE = 'SendAdditionalAttribute'
    SEND_CLASSIFICATION = 'SendClassification'
    SEND_EMAIL_MO_KEYWORD = 'SendEmailMOKeyword'
    SEND_SMS_MO_KEYWORD = 'SendSMSMOKeyword'
    SENDER_PROFILE = 'SenderProfile'
    SUBSCRIBER_SEND_RESULT = 'SubscriberSendResult'
    SUPPRESSION_LIST_CONTEXT = 'SuppressionListContext'
    SUPPRESSION_LIST_DEFINITION = 'SuppressionListDefinition'
    SURVEY_EVENT = 'SurveyEvent'
    TIMEZONE = 'TimeZone'
    TRIGGERED_SEND_DEFINITION = 'TriggeredSendDefinition'
    TRIGGERED_SEND_SUMMARY = 'TriggeredSendSummary'
    UNSUBSCRIBE_FROM_SMS_PUBLICATION_MO_KEYWORD = 'UnsubscribeFromSMSPublicationMOKeyword'


class FolderType:

    AB_TEST = 'ABTest'
    ASSET = 'asset'
    SIMPLE_AUTOMATED_EMAILS = 'automated_email'
    AUTOMATIONS = 'automations'
    BUILD_AUDIENCE_ACTIVITY = 'BuildAudienceActivity'
    CAMPAIGN = 'campaign'
    CONDENSED_PREVIEW = 'condensedlpview'
    MY_CONTENTS = 'content'
    CONTEXTUAL_SUPPRESSION_LIST = 'contextual_suppression_list'
    DATA_EXTENSIONS = 'dataextension'
    MY_DOCUMENTS = 'document'
    ELT_ACTIVITY = 'ELTactivity'
    MY_EMAILS = 'email'
    EMAIL_HIDDEN_MESSAGE_MODEL = 'email_hidden_messagemodel'
    FILTER_ACTIVITIES = 'filteractivity'
    DATA_FILTERS = 'filterdefinition'
    GLOBAL_EMAIL = 'global_email'
    GLOBAL_EMAIL_SUBSCRIBERS = 'global_email_sub'
    MY_GROUPS = 'group'
    HIDDEN = 'Hidden'
    MY_IMAGES = 'image'
    MY_TRACKING = 'job'
    MY_LISTS = 'list'
    LIVE_CONTENT = 'livecontent'
    MEASURES = 'measure'
    PORTFOLIO = 'media'
    MESSAGE = 'message'
    MICROSITES = 'microsite'
    MICROSITE_LAYOUTS = 'micrositelayout'
    MY_SUBSCRIBERS = 'mysubs'
    ORGANIZATIONS = 'organization'
    PLAYBOOKS = 'playbooks'
    PROGRAMS = 'programs2'
    PUBLICATION_LISTS = 'publication'
    QUERY_ACTIVITY = 'queryactivity'
    SALESFORCE_DATA_EXTENSION = 'salesforcedataextension'
    SALESFORCE_SENDS = 'salesforcesends'
    SALESFORCE_SENDS_V5 = 'salesforcesendsv5'
    SHARED_CONTENT = 'shared_content'
    SHARED_CONTEXTUAL_SUPPRESSION_LIST = 'shared_contextual_suppression_list'
    SHARED_DATA = 'shared_data'
    SHARED_DATA_EXTENSIONS = 'shared_dataextension'
    SHARED_EMAIL_MESSAGES = 'shared_email'
    SHARED_ITEMS = 'shared_item'
    SHARED_PORTFOLIOS = 'shared_portfolio'
    SHARED_PUBLICATION_LISTS = 'shared_publication'
    SHARED_SALESFORCE_DATA_EXTENSION = 'shared_salesforcedataextension'
    SHARED_SUPPRESSION_LISTS = 'shared_suppression_list'
    SHARED_SURVEYS = 'shared_survey'
    SHARED_TEMPLATES = 'shared_template'
    SSJS_ACTIVITY = 'ssjsactivity'
    SUPPRESSION_LISTS = 'suppression_list'
    MY_SURVEYS = 'survey'
    SYNCHRONIZED_DATA_EXTENSION = 'synchronizeddataextension'
    MY_TEMPLATES = 'template'
    TRIGGERED_SENDS = 'triggered_send'
    TRIGGERED_SENDS_JOURNEY_BUILDER = 'triggered_send_journeybuilder'
    USER_INITIATED_SENDS = 'userinitiatedsends'


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


class ET_Perform(FuelSDK.rest.ET_Constructor):
    def __init__(self, auth_stub, action, object_source=None, object_type=None):
        auth_stub.refresh_token()

        if object_type:
            ws_definition = auth_stub.soap_client.factory.create(object_type)
        else:
            ws_definition = auth_stub.soap_client.factory.create(type(object_source).__name__)

        if object_source.CustomerKey:
            ws_definition.CustomerKey = object_source.CustomerKey
        if object_source.ObjectID:
            ws_definition.ObjectID = object_source.ObjectID

        response = None
        try:
            response = auth_stub.soap_client.service.Perform(Action=action, Definitions={"Definition": ws_definition})
        except suds.TypeNotFound:
            pass

        if response is not None:
            super(ET_Perform, self).__init__(response)


class ET_Extract(FuelSDK.rest.ET_Constructor):
    def __init__(self, auth_stub, parameters):
        auth_stub.refresh_token()

        ws_extractRequest = auth_stub.soap_client.factory.create('ExtractRequest')
        ws_extractRequest.Options = auth_stub.soap_client.factory.create('ExtractOptions')
        ws_extractRequest.ID = "c7219016-a7f0-4c72-8657-1ec12c28a0db"

        ws_parameters = []
        for name, value in parameters.items():
            ws_parameter = auth_stub.soap_client.factory.create("ExtractParameter")
            ws_parameter.Name = name
            if isinstance(value, date) or isinstance(value, datetime):
                ws_parameter.Value = value.strftime("%m/%d/%Y 12:00:00 AM")
            else:
                ws_parameter.Value = value
            ws_parameters.append(ws_parameter)
        ws_extractRequest.Parameters.Parameter = ws_parameters

        response = None
        try:
            response = auth_stub.soap_client.service.Extract(ws_extractRequest)
        except suds.TypeNotFound as e:
            if e.message != "Type not found: 'ExtractResult'":
                raise e

        if response is not None:
            super(ET_Extract, self).__init__(response)


def search_filter(property_name, operator, value):
    return simple_filter(property_name, operator, value)


def simple_filter(property_name, operator, value):
    value_type = 'Value'
    if isinstance(value, date) or isinstance(value, datetime):
        value_type = 'DateValue'

    return {
        'Property': property_name,
        'SimpleOperator': operator,
        value_type: value
    }


def complex_filter(left_operand, logical_operator, right_operand):
    logical_operator = logical_operator.upper()
    if logical_operator not in ('AND', 'OR'):
        raise ValueError("Invalid Logical Operator, must be AND or OR.")

    return {
        'LeftOperand': left_operand,
        'LogicalOperator': logical_operator,
        'RightOperand': right_operand
    }


class ET_API:

    client = None
    current_object = None

    def __init__(self, get_server_wsdl=False, debug=False, params=None):
        if debug:
            logger_debug.setLevel(logging.DEBUG)

        self.client = FuelSDK.ET_Client(get_server_wsdl=get_server_wsdl, debug=debug, params=params)

    class ETApiError(Exception):
        pass

    class ObjectAlreadyExists(Exception):
        pass

    class ObjectDoesntExist(Exception):
        pass

    @staticmethod
    def check_response(response):
        if response.message and response.message not in ('OK', 'MoreDataAvailable'):
            if len(response.results) > 0 and 'already in use' in getattr(response.results[0], "StatusMessage", ""):
                raise ET_API.ObjectAlreadyExists('Object already exists')
            elif len(response.results) > 0 and 'Concurrency violation' in getattr(response.results[0], "ErrorMessage", ""):
                raise ET_API.ObjectDoesntExist("Object doesn't exist")
            elif len(response.results) > 0 and getattr(response.results[0], "StatusMessage", ""):
                raise ET_API.ETApiError('Error: {}'.format(getattr(response.results[0], "StatusMessage", "")))
            elif len(response.results) > 0 and len(getattr(response.results, "Result", [])) > 0 and getattr(response.results.Result[0], "StatusMessage", ""):
                raise ET_API.ETApiError('{}'.format(response.results.Result[0].StatusMessage))
            else:
                raise ET_API.ETApiError('{}'.format(response.message))

        logger_debug.debug('Post Status: {}; Code: {}; Message: {}; Result Count: {}'
                           .format(response.status, response.code, response.message, len(response.results)))

    def get_client(self):
        if not self.client:
            self.__init__()
        return self.client

    def parse_object(self, object_type, properties):
        return FuelSDK.rest.ET_Constructor().parse_props_into_ws_object(self.get_client(), object_type, properties)

    def get_object_class(self, object_type, is_rest=False):
        try:
            if object_type.startswith('ET_'):
                self.current_object = getattr(FuelSDK, object_type)()
            else:
                self.current_object = getattr(FuelSDK, 'ET_{}'.format(object_type))()
        except AttributeError:
            if is_rest:
                self.current_object = globals()['ET_ObjectRest'](object_type)
            else:
                self.current_object = globals()['ET_Object'](object_type)

        self.current_object.auth_stub = self.get_client()
        return self.current_object

    def get_info(self, object_type):
        obj = self.get_object_class(object_type)
        try:
            return obj.info().results[0].Properties
        except IndexError:
            return []

    def perform_action(self, action, object_source=None, object_type=None):
        auth_stub = self.get_client()
        res = ET_Perform(auth_stub, action, object_source, object_type)
        return res

    def extract_data(self, parameters):
        auth_stub = self.get_client()
        res = ET_Extract(auth_stub, parameters)
        return res

    @validate_response()
    def get_objects(self, object_type, search_filter=None, property_list=None, query_all_accounts=False, is_rest=False):
        obj = self.get_object_class(object_type, is_rest)
        if search_filter:
            obj.search_filter = search_filter
        if property_list:
            obj.props = property_list
        if query_all_accounts:
            obj.QueryAllAccounts = True
        return obj.get()

    @validate_response()
    def get_more_results(self):
        return self.current_object.getMoreResults()

    @validate_response()
    def create_object(self, object_type, property_dict, data_extension_key=None, is_rest=False):
        obj = self.get_object_class(object_type, is_rest)
        if object_type == ObjectType.DATA_EXTENSION_ROW:
            obj.CustomerKey = data_extension_key
        obj.props = property_dict
        return obj.post()

    @validate_response()
    def update_object(self, object_type, object_id_dict=None, values_dict=None, data_extension_key=None, is_rest=False):
        obj = self.get_object_class(object_type, is_rest)
        if object_type in (ObjectType.DATA_EXTENSION_ROW, ObjectType.DATA_EXTENSION_COLUMN):
            obj.CustomerKey = data_extension_key
            obj.props = values_dict
        else:
            obj.props = object_id_dict
            obj.props.update(values_dict)
        return obj.patch()

    @validate_response()
    def delete_object(self, object_type, object_id_dict=None, data_extension_key=None, data_extension_name=None, is_rest=False):
        obj = self.get_object_class(object_type, is_rest)
        if object_type == ObjectType.DATA_EXTENSION_ROW:
            if not data_extension_key:
                raise self.ETApiError("data_extension_key parameters missing.")
            obj.CustomerKey = data_extension_key
            if data_extension_name:
                obj.Name = data_extension_name
        if object_id_dict:
            obj.props = object_id_dict
        return obj.delete()

    # Specific methods
    def get_data_extension_columns(self, customer_key, property_list=None):
        search_filter_object = simple_filter('DataExtension.CustomerKey', Operator.EQUALS, customer_key)
        return self.get_objects(ObjectType.DATA_EXTENSION_COLUMN, search_filter_object, property_list)

    def get_list_subscriber(self, search_filter=None, property_list=None):
        return self.get_objects(ObjectType.LIST_SUBSCRIBER, search_filter, property_list)

    def get_data_extension_rows(self, customer_key, search_filter=None, property_list=None):
        de_row = FuelSDK.ET_DataExtension_Row()
        de_row.auth_stub = self.get_client()
        de_row.CustomerKey = customer_key
        if search_filter:
            de_row.search_filter = search_filter
        if property_list:
            de_row.props = property_list
        return de_row.get()

    def create_data_extension_rows(self, data_extension_key, keys_list, values_list):
        endpoint = 'https://www.exacttargetapis.com/hub/v1/dataevents/key:{}/rowset'.format(data_extension_key)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(self.client.authToken)}

        if len(keys_list) != len(values_list):
            raise self.ETApiError("keys_list and values_list must be the same size.")

        payload = []
        for i, values in enumerate(values_list):
            payload.append({"keys": keys_list[i], "values": values})

        r = requests.post(endpoint, json=payload, headers=headers)
        res = FuelSDK.rest.ET_Constructor(r, True)

        if res.code == 200:
            return res
        else:  # Endpoint unavailable - Insert row by row
            rows_inserted = 0
            for keys_values in payload:
                property_dict = {}
                for i, key in enumerate(keys_values["keys"]):
                    property_dict[key] = keys_values["values"][i]
                res = self.create_object(ObjectType.DATA_EXTENSION_ROW, property_dict, data_extension_key)
                if res.code == 200:
                    rows_inserted += 1
            return rows_inserted

    # Convenience methods
    @validate_response()
    def add_subscriber_to_list(self, email, list_ids, subscriber_key=None):
        return self.get_client().AddSubscriberToList(email, list_ids, subscriber_key)

    @validate_response()
    def create_data_extension(self, name, columns, customer_key=None, category_id=None, sendable_de_field_name=None, sendable_subscriber_field_name=None):
        data_extension = {
            'Name': name,
            'columns': columns
        }

        if customer_key:
            data_extension['CustomerKey'] = customer_key

        if category_id:
            data_extension['CategoryID'] = category_id

        if sendable_de_field_name and sendable_subscriber_field_name:
            data_extension['IsSendable'] = True
            data_extension['SendableDataExtensionField'] = {
                "Name": sendable_de_field_name
            }
            data_extension['SendableSubscriberField'] = {
                "Name": sendable_subscriber_field_name
            }

        return self.get_client().CreateDataExtensions([data_extension])

    def clear_data_extension(self, data_extension_key):
        res = self.get_objects(ObjectType.DATA_EXTENSION,
                               simple_filter("CustomerKey", Operator.EQUALS, data_extension_key),
                               property_list=["CustomerKey", "ObjectID", "Name"])

        if len(res.results) == 0:
            raise self.ETApiError("The Data Extension {} wasn't found.".format(data_extension_key))

        try:
            return self.clear_data_extension_action(res.results[0])
        except self.ETApiError as e:  # ClearData action only available on Enterprise 2.0 accounts - Delete all rows
            res = self.get_data_extension_columns(data_extension_key)
            columns = [c.Name for c in res.results if c.IsPrimaryKey]
            if not columns:
                raise e
            res = self.get_data_extension_rows(data_extension_key, property_list=columns)
            for row in res.results:
                fields_data = {}
                for prop in row.Properties.Property:
                    fields_data[prop["Name"]] = prop["Value"]
                res = self.delete_object(ObjectType.DATA_EXTENSION_ROW, object_id_dict=fields_data,
                                         data_extension_key=data_extension_key)
            return len(res.results)

    @validate_response()
    def clear_data_extension_action(self, data_extension_object):
        return self.perform_action("ClearData", data_extension_object, "DataExtension")

    @validate_response()
    def start_automation(self, automation_key):
        res = self.get_objects(ObjectType.AUTOMATION,
                               simple_filter("CustomerKey", Operator.EQUALS, automation_key),
                               property_list=["CustomerKey", "ProgramID", "Name"])

        if len(res.results) == 0:
            raise self.ETApiError("The Automation {} wasn't found.".format(automation_key))

        aut_object = res.results[0]
        aut = self.get_client().soap_client.factory.create("Automation")
        aut.Name = aut_object.Name
        aut.CustomerKey = aut_object.CustomerKey
        aut.ObjectID = aut_object.ObjectID

        return self.perform_action("Start", aut, "Automation")

    def create_campaign(self, name, description, campaign_code, color='Public', is_favorite=False):
        if color not in ('Public', 'Private'):
            raise self.ETApiError('Invalid color, must be: Public or Private')

        property_dict = {
            'name': name,
            'description': description,
            'campaignCode': campaign_code,
            'color': color,
            'favorite': is_favorite
        }
        return self.create_object(ObjectType.CAMPAIGN, property_dict)

    def create_or_update_html_paste_email(self, customer_key, category_id, name, subject, pre_header, html, plain_text):
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

    def get_or_update_user_initiated_email(self, subscription_name, email_name):
        res = self.get_objects(
            object_type='EmailSendDefinition',
            search_filter=simple_filter('Name', Operator.EQUALS, subscription_name),
            property_list=['Email.ID']
        )
        try:
            email_id = res.results[-1].Email.ID
            res = self.get_objects(
                object_type=ObjectType.EMAIL,
                search_filter=simple_filter('ID', Operator.EQUALS, email_id),
                property_list=['Name']
            )
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

    def send_trigger_email(self, trigger_key, email_address, subscriber_key, attributes=None):
        token = self.get_client().authToken
        url = "https://www.exacttargetapis.com/messaging/v1/messageDefinitionSends/key:{}/send".format(trigger_key)
        data = {
            "To": {
                "Address": email_address,
                "SubscriberKey": subscriber_key,
                "ContactAttributes": {
                    "SubscriberAttributes": attributes or {}
                }
            },
            "OPTIONS": {
                "RequestType": "ASYNC"
            }
        }
        res = requests.post(url, json=data, headers={"Authorization": "Bearer {}".format(token)})
        return res

    def get_folder_full_path(self, folder_id):
        res = self.get_objects(ObjectType.FOLDER, simple_filter("ID", Operator.EQUALS, folder_id))
        full_path_array = [res.results[0].Name]
        folder_id = res.results[0].ParentFolder.ID
        while folder_id != 0:
            res = self.get_objects(ObjectType.FOLDER, simple_filter("ID", Operator.EQUALS, folder_id))
            full_path_array.append(res.results[0].Name)
            folder_id = res.results[0].ParentFolder.ID
        full_path = full_path_array[-1]
        for i, folder_name in reversed(list(enumerate(full_path_array))):
            if i == len(full_path_array) - 1:
                continue
            full_path += " > " + folder_name
        return full_path

    def get_or_create_folder_hierarchy(self, folders_type, folder_names):
        last_folder_id = None

        for folder_name in folder_names:
            last_folder_id = self.get_or_create_folder(folders_type, folder_name, last_folder_id)

        return last_folder_id

    def get_or_create_folder(self, folder_type, folder_name, parent_folder_id=None):
        main_filter = complex_filter(
            simple_filter("Name", Operator.EQUALS, folder_name),
            "AND",
            simple_filter("ContentType", Operator.EQUALS, folder_type)
        )

        if parent_folder_id:
            main_filter = complex_filter(
                simple_filter("Name", Operator.EQUALS, folder_name),
                "AND",
                simple_filter("ParentFolder.ID", Operator.EQUALS, parent_folder_id)
            )

        res = self.get_objects(ObjectType.FOLDER, main_filter, property_list=["ID"])
        if len(res.results) > 0:
            return res.results[0].ID

        properties = {
            "Name": folder_name,
            "ContentType": folder_type,
            "Description": "",
            "AllowChildren": True,
            "IsEditable": True,
            "IsActive": True,
            "ParentFolder": {}
        }
        if parent_folder_id:
            properties["ParentFolder"] = {"ID": parent_folder_id}
        else:
            res = self.get_objects(ObjectType.FOLDER,
                                   complex_filter(
                                       simple_filter("ContentType", Operator.EQUALS, folder_type),
                                       "AND",
                                       simple_filter("ParentFolder.ID", Operator.EQUALS, 0)),
                                   property_list=["Name", "ID", "ContentType", "ParentFolder.ID"])
            properties["ParentFolder"] = {"ID": res.results[0].ID}

        res = self.create_object(ObjectType.FOLDER, property_dict=properties)
        if res.status:
            return self.get_or_create_folder(folder_type, folder_name)

    def get_contacts_counts(self):
        token = self.get_client().authToken
        url = "https://www.exacttargetapis.com/contacts/v1/addresses/count/"
        res = requests.post(url, headers={"Authorization": "Bearer {}".format(token)})
        return res.json().get("totalCount", -1)
