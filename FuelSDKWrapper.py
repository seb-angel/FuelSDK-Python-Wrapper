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
    CONTENT_BUILDER = 'CONTENT_BUILDER'
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


def search_filter_for_rest_call(search_filter):
    if 'LeftOperand' in search_filter:  # Complex Filter
        left_operand = search_filter_for_rest_call(search_filter['LeftOperand'])
        logical_operator = search_filter['LogicalOperator']
        right_operand = search_filter_for_rest_call(search_filter['RightOperand'])
        return "{}%20{}%20{}".format(left_operand, logical_operator, right_operand)
    else:  # Simple Filter
        prop = search_filter['Property']
        operator = operator_for_rest_call(search_filter['SimpleOperator'])
        value = search_filter.get('Value', search_filter.get('DateValue'))
        if operator == 'like':
            value = value.replace('%', '%25')
        return "{}%20{}%20'{}'".format(prop, operator, value)


def operator_for_rest_call(operator):
    operators = {
        'equals': 'eq',
        'notEquals': 'neq',
        'greaterThan': 'gt',
        'greaterThanOrEqual': 'gte',
        'lessThan': 'lt',
        'lessThanOrEqual': 'lte',
        'like': 'like'
    }
    return operators[operator]


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
            if len(response.results) > 0 and 'already in use' in (getattr(response.results[0], "StatusMessage", "") or ""):
                raise ET_API.ObjectAlreadyExists('Object already exists')
            elif len(response.results) > 0 and 'Concurrency violation' in (getattr(response.results[0], "ErrorMessage", "") or ""):
                raise ET_API.ObjectDoesntExist("Object doesn't exist")
            elif len(response.results) > 0 and getattr(response.results[0], "ValueErrors", "") and len(response.results[0].ValueErrors.ValueError) > 0:
                raise ET_API.ETApiError('{}'.format(response.results[0].ValueErrors.ValueError[0].ErrorMessage))
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

    def get_data_extension_rows_rest(self, customer_key, search_filter=None, property_list=None, order_by=None, page_size=None, page=None, max_rows=2500):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(self.client.authToken)}
        endpoint = "{}data/v1/customobjectdata/key/{}/rowset?".format(self.client.base_api_url, customer_key)

        if search_filter:
            endpoint += "&$filter={}".format(search_filter_for_rest_call(search_filter))

        if property_list:
            endpoint += "&$fields={}".format(",".join(property_list))

        if order_by:
            endpoint += "&$orderBy={}".format(order_by)

        if page_size:
            endpoint += "&$pagesize={}".format(page_size)

        if page:
            endpoint += "&$page={}".format(page)

        if max_rows < 0:
            max_rows = 2500

        result = []
        r = requests.get(endpoint, headers=headers)
        items_count = r.json()['count']
        if r.status_code in range(200, 300) and items_count:
            result = r.json()['items'][:max_rows]
            if not page:
                while 'next' in r.json()['links'] and len(result) < max_rows:
                    endpoint = '{}data{}'.format(self.client.base_api_url, r.json()['links']['next'])
                    r = requests.get(endpoint, headers=headers)
                    if r.status_code in range(200, 300) and r.json()['items']:
                        result += r.json()['items'][:max_rows-len(result)]
        return result, items_count

    def get_data_extension_rows(self, customer_key, search_filter=None, property_list=None):
        de_row = FuelSDK.ET_DataExtension_Row()
        de_row.auth_stub = self.get_client()
        de_row.CustomerKey = customer_key
        if search_filter:
            de_row.search_filter = search_filter
        if property_list:
            de_row.props = property_list
        return de_row.get()

    def run_async_call(self, endpoint, method, payload):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(self.client.authToken)}
        if method == "POST":
            r = requests.post(endpoint, json=payload, headers=headers)
        elif method == "PUT":
            r = requests.put(endpoint, json=payload, headers=headers)
        else:
            raise self.ETApiError("Invalid Method.")

        if r.status_code in range(200, 300):
            request_id = r.json()['requestId']
            endpoint = '{}/data/v1/async/{}/status'.format(self.client.base_api_url, request_id)
            status = 'Pending'
            while status == 'Pending':
                r = requests.get(endpoint, headers=headers)
                if r.status_code in range(200, 300):
                    status = r.json()["status"]["requestStatus"]
        return r

    def create_data_extension_rows(self, data_extension_key, keys_list, values_list):
        endpoint = '{}hub/v1/dataevents/key:{}/rowset'.format(self.client.base_api_url, data_extension_key)

        if len(keys_list) != len(values_list):
            raise self.ETApiError("keys_list and values_list must be the same size.")

        payload = []
        for i, values in enumerate(values_list):
            payload.append({"keys": keys_list[i], "values": values})

        token = self.get_client().authToken
        res = requests.post(endpoint, json=payload, headers={"Authorization": "Bearer {}".format(token)})
        return res

    def create_data_extension_rows_async(self, data_extension_key, rows_list):
        endpoint = '{}/data/v1/async/dataextensions/key:{}/rows'.format(self.client.base_api_url, data_extension_key)
        payload = {'items': rows_list}
        res = self.run_async_call(endpoint, "POST", payload)
        return res

    def upsert_data_extension_rows_async(self, data_extension_key, rows_list):
        endpoint = '{}/data/v1/async/dataextensions/key:{}/rows'.format(self.client.base_api_url, data_extension_key)
        payload = {'items': rows_list}
        res = self.run_async_call(endpoint, "PUT", payload)
        return res

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

    def copy_data_extension(self, source_customer_key, new_name, new_customer_key=None, new_category_id=None,
                            keep_template=True, keep_retention_policy=True, keep_sendable=True):
        source_data_extension = self.get_objects(ObjectType.DATA_EXTENSION,
                                                 simple_filter("CustomerKey", Operator.EQUALS, source_customer_key),
                                                 property_list=['CustomerKey', 'Name', 'Description', 'IsSendable',
                                                                'IsTestable', 'SendableDataExtensionField.Name',
                                                                'SendableSubscriberField.Name', 'Template.CustomerKey',
                                                                'CategoryID', 'DataRetentionPeriodLength',
                                                                'DataRetentionPeriodUnitOfMeasure', 'RowBasedRetention',
                                                                'ResetRetentionPeriodOnImport',
                                                                'DeleteAtEndOfRetentionPeriod',
                                                                'RetainUntil', 'DataRetentionPeriod'])

        if source_data_extension.status and source_data_extension.results:
            source_data_extension = source_data_extension.results[0]
        else:
            raise self.ETApiError("The Data Extension wasn't found with the given CustomerKey.")

        source_columns = self.get_data_extension_columns(source_customer_key)
        new_columns = []
        for source_column in sorted(source_columns.results, key=lambda i: i.Ordinal):
            new_column = {
                'DefaultValue': source_column.DefaultValue,
                'FieldType': source_column.FieldType,
                'IsPrimaryKey': source_column.IsPrimaryKey,
                'IsRequired': source_column.IsRequired,
                'Name': source_column.Name,
                'StorageType': source_column.StorageType
            }
            if "MaxLength" in source_column:
                new_column["MaxLength"] = source_column.MaxLength
            if "Scale" in source_column:
                new_column["Scale"] = source_column.Scale
            new_columns.append(new_column)

        data_extension = {
            'Name': new_name,
            'columns': new_columns,
            'Description': source_data_extension.Description
        }

        if new_customer_key:
            data_extension['CustomerKey'] = new_customer_key

        if new_category_id:
            data_extension['CategoryID'] = new_category_id

        if keep_sendable and "SendableDataExtensionField" in source_data_extension and "SendableSubscriberField" in source_data_extension:
            data_extension['IsSendable'] = source_data_extension.IsSendable
            data_extension['IsTestable'] = source_data_extension.IsTestable

            if "Subscriber" in source_data_extension.SendableSubscriberField.Name:
                sendable_subscriber_field_name = "Subscriber Key"
            elif "Email" in source_data_extension.SendableSubscriberField.Name:
                sendable_subscriber_field_name = "Email Address"
            else:
                raise self.ETApiError("The Sendable Subscriber Field is invalid.")

            data_extension['SendableDataExtensionField'] = {
                "Name": source_data_extension.SendableDataExtensionField.Name
            }
            data_extension['SendableSubscriberField'] = {
                "Name": sendable_subscriber_field_name
            }

        if keep_template and "Template" in source_data_extension:
            data_extension['Template'] = {
                'CustomerKey': source_data_extension.Template.CustomerKey
            }

        if keep_retention_policy:
            data_extension['RowBasedRetention'] = source_data_extension.RowBasedRetention
            data_extension['ResetRetentionPeriodOnImport'] = source_data_extension.ResetRetentionPeriodOnImport
            data_extension['DeleteAtEndOfRetentionPeriod'] = source_data_extension.DeleteAtEndOfRetentionPeriod
            data_extension['RetainUntil'] = source_data_extension.RetainUntil

            if "DataRetentionPeriod" in source_data_extension \
                    and "DataRetentionPeriodLength" in source_data_extension \
                    and "DataRetentionPeriodUnitOfMeasure" in source_data_extension:
                data_extension['DataRetentionPeriod'] = source_data_extension.DataRetentionPeriod
                data_extension['DataRetentionPeriodLength'] = source_data_extension.DataRetentionPeriodLength
                data_extension[
                    'DataRetentionPeriodUnitOfMeasure'] = source_data_extension.DataRetentionPeriodUnitOfMeasure

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

    def create_or_update_html_paste_email(self, category_id, name, subject, html, customer_key=None, plain_text=None, pre_header=None):
        payload = {
            "name": name,
            "category": {
                "id": category_id
            },
            "channels": {
                "email": True,
                "web": False
            },
            "views": {
                "html": {
                    "content": html
                },
                "subjectline": {
                    "content": subject
                }
            },
            "assetType": {
                "name": "htmlemail",
                "id": 208
            },
            "data": {
                "email": {
                    "options": {
                        "characterEncoding": "utf-8"
                    }
                }
            }
        }

        if customer_key:
            payload["customerKey"] = customer_key

        if plain_text:
            payload["views"]["text"] = {
                "content": plain_text
            }

        if pre_header:
            payload["views"]["preheader"] = {
                "content": pre_header
            }

        headers = {"Authorization": "Bearer {}".format(self.get_client().authToken)}
        url = "{}asset/v1/content/assets".format(self.get_client().base_api_url)

        # Create Asset
        res = requests.post(url, json=payload, headers=headers)
        if res.status_code not in range(200, 300):  # Creation failed, try Update instead
            # Retrieve Asset by Customer Key if provided, Name otherwise
            if customer_key:
                res = requests.get("{}?$filter=customerKey%20eq%20'{}'".format(url, customer_key), headers=headers)
            else:
                res = requests.get("{}?$filter=name%20eq%20'{}'".format(url, name), headers=headers)

            if res.status_code in range(200, 300):
                data = res.json()
                if data["count"] == 1:  # Asset found, Update Asset
                    asset_id = data["items"][0]["id"]
                    res = requests.patch("{}/{}".format(url, asset_id), json=payload, headers=headers)
        return res

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
            if folders_type == FolderType.CONTENT_BUILDER:
                last_folder_id = self.get_or_create_content_builder_folder(folder_name, last_folder_id)
            else:
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

    def get_or_create_content_builder_folder(self, folder_name, parent_folder_id=None):
        headers = {"Authorization": "Bearer {}".format(self.get_client().authToken)}
        url = "{}asset/v1/content/categories".format(self.get_client().base_api_url)
        if not parent_folder_id:  # Retrieve the folder with parentID = 0, this is the root folder
            res = requests.get("{}?$filter=parentId eq 0".format(url), headers=headers)
            parent_folder_id = res.json()["items"][0]["id"]

        res = requests.get("{}?$filter=parentId eq {}".format(url, parent_folder_id), headers=headers)
        if res.json()["count"] > 0:  # Retrieve all the folders that has this parent folder
            for folder in res.json()["items"]:
                if folder["name"] == folder_name:  # Stop if folder is found
                    return folder["id"]

        # The folder doesn't exist, create it
        payload = {
            "Name": folder_name,
            "ParentId": parent_folder_id
        }
        res = requests.post(url, json=payload, headers=headers)
        return res.json()["id"]

    def get_contacts_counts(self):
        token = self.get_client().authToken
        url = "https://www.exacttargetapis.com/contacts/v1/addresses/count/"
        res = requests.post(url, headers={"Authorization": "Bearer {}".format(token)})
        return res.json().get("totalCount", -1)

    def get_email_preview(self, email_id, list_id=None, data_extension_key=None, contact_id=None, contact_key=None):
        url = "{}guide/v1/emails/{}".format(self.get_client().base_api_url, email_id)

        if list_id:
            url += "/lists/{}".format(list_id)
        elif data_extension_key:
            url += "/dataExtension/key:{}".format(data_extension_key)
        else:
            raise self.ETApiError("list_id or data_extension_key required.")

        if contact_id:
            url += "/contacts/{}/preview?kind=html,text".format(contact_id)
        elif contact_key:
            url += "/contacts/key:{}/preview?kind=html,text".format(contact_key)
        else:
            raise self.ETApiError("contact_id or contact_key required.")

        token = self.get_client().authToken
        res = requests.post(url, headers={"Authorization": "Bearer {}".format(token)})
        return res.json()
