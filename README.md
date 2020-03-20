# FuelSDKWrapper
Simplify and enhance the FuelSDK for Salesforce Marketing Cloud (ExactTarget).

## Overview
The Fuel SDK Wrapper for Python adds functionalities to the default Fuel SDK and provides access to more SOAP API objects. The Fuel SDK documentation can be found [here](https://github.com/salesforce-marketingcloud/FuelSDK-Python).

## Installation
```python
pip install FuelSDKWrapper
```

## Getting Started

### Configuring

You must configure your access tokens and details for the Fuel SDK in one of the following two ways.

1. Copy the included `config.python.template` file to `config.python` in either `~/.fuelsdk/`, within this python module or at the root of your project.
2. Add environment variables:
    * `FUELSDK_CLIENT_ID` (required)
    * `FUELSDK_CLIENT_SECRET` (required)
    * `FUELSDK_APP_SIGNATURE`
    * `FUELSDK_DEFAULT_WSDL`
    * `FUELSDK_AUTH_URL`
    * `FUELSDK_WSDL_FILE_LOCAL_LOC`

Edit `config.python` or declare environment variables so you can input the ClientID and Client Secret values provided when you registered your application. If you are building a HubExchange application for the Interactive Marketing Hub then, you must also provide the Application Signature (`appsignature` / `FUELSDK_APP_SIGNATURE`).
The `defaultwsdl` / `FUELSDK_DEFAULT_WSDL` configuration must be [changed depending on the ExactTarget service](https://code.exacttarget.com/question/there-any-cetificrate-install-our-server-access-et-api "ExactTarget Forum").
The `authenticationurl` / `FUELSDK_AUTH_URL` must also be [changed depending on service](https://code.exacttarget.com/question/not-able-create-accesstoken-when-clientidsecret-associated-preproduction-account "ExactTarget Forum").
The `wsdl_file_local_loc` / `FUELSDK_WSDL_FILE_LOCAL_LOC` allows you to specify the full path/filename where the WSDL file will be located on disk, if for instance you are connecting to different endpoints from the same server.

If you have not registered your application or you need to lookup your Application Key or Application Signature values, please go to App Center at [Code@: ExactTarget's Developer Community](http://code.exacttarget.com/appcenter "Code@ App Center").


| Environment | WSDL (default) | URL (auth) |
| ----------- | -------------- | ---------- |
| Production  | https://webservice.exacttarget.com/etframework.wsdl | https://auth.exacttargetapis.com/v1/requestToken?legacy=1 |
| Sandbox     | https://webservice.test.exacttarget.com/Service.asmx?wsdl | https://auth-test.exacttargetapis.com/v1/requestToken?legacy=1 |


It is also possible to pass those values directly to the API object:
```python
params = {
    "clientid": "YOUR_CLIENT_ID",
    "clientsecret": "YOUR_CLIENT_SECRET"
}
api = ET_API(params=params)
```

## Examples

### Get the List objects

```python
# Add a require statement to reference the FuelSDK functionality
from FuelSDKWrapper import ET_API, ObjectType

# Next, create an instance of the ET_API class
api = ET_API()

# Get the List objects
response = api.get_objects(ObjectType.LIST)

# Print out the results for viewing
print('Post Status: {}'.format(response.status))
print('Code: {}'.format(response.code))
print('Message: {}'.format(response.message))
print('Result Count: {}'.format(len(response.results)))
print('Results: {}'.format(response.results))
```

### Some examples of utilization

```python
from FuelSDKWrapper import ET_API, ObjectType, Operator, FolderType, simple_filter, complex_filter
from datetime import datetime, timedelta

api = ET_API()

# Get Subscriber Data using the IN Operator
response = api.get_objects(
    ObjectType.SUBSCRIBER,
    simple_filter("EmailAddress", Operator.IN, ["my.email@domain.com", "your.email@domain.com"])
)

# Find Query Definition using the LIKE Operator
response = api.get_objects(
    ObjectType.QUERY_DEFINITION,
    simple_filter("QueryText", Operator.LIKE, "FROM My_DE"),
    property_list=["Name", "CategoryID", "QueryText"]
)

# Get Jobs sent in the last 30 days
start_date = datetime.now() - timedelta(days=30)
response = api.get_objects(
    ObjectType.SEND,
    simple_filter("SendDate", Operator.GREATER_THAN, start_date)
)

# Get Folder Data
response = api.get_objects(
    ObjectType.FOLDER,
    complex_filter(
        simple_filter("Name", Operator.EQUALS, "My_Folder_Name"),
        "OR",
        simple_filter("Name", Operator.EQUALS, "My_Other_Folder_Name")
    ),
    property_list=["ID", "Name"]
)

# Get Folder Full Path
folder_id = 12345
response = api.get_folder_full_path(folder_id)

# Get or Create Folder Full Path
folder_names = ["Test", "Sub_Test"]
folder_type = FolderType.DATA_EXTENSIONS
response = api.get_or_create_folder_hierarchy(folder_type, folder_names)

# Start an Automation
response = api.start_automation("Automation_Key")

# Seng Trigger Email
response = api.send_trigger_email("MyTriggerKey", "email@email.com", "subscriberkey@email.com", attributes={
    "first_nm": "Sebastien",
    "birth_dt": "1/1/1990"
})

# Get Tokens
short_token = api.get_client().authToken
long_token = api.get_client().internalAuthToken

# Get Data Extension Fields sorted by Ordinal
fields = sorted(api.get_data_extension_columns("My_DE_Key").results, key=lambda x: x.Ordinal)

# Clear Data Extension
response = api.clear_data_extension("DE_Key")

# Create Batch of Data Extension Rows
# Synchronous
keys_list = [
    ["Field1", "Field2", "Field3"],  # Fields for Row 1
    ["Field1", "Field2", "Field3"],  # Fields for Row 2
    ["Field1", "Field2", "Field3"]   # Fields for Row 3
]
values_list = [
    ["Row1_Value1", "Row1_Value2", "Row1_Value3"],
    ["Row2_Value1", "Row2_Value2", "Row2_Value3"],
    ["Row3_Value1", "Row3_Value2", "Row3_Value3"]
]
rows_inserted_count = api.create_data_extension_rows("DE_Key", keys_list, values_list)

# Asynchronous Insert and Upsert
items_list = [
    {"Field1": "Value1", "Field2": "Value2", "Field3": "Value3"},  # Row 1
    {"Field1": "Value1", "Field2": "Value2", "Field3": "Value3"},  # Row 2
    {"Field1": "Value1", "Field2": "Value2", "Field3": "Value3"}  # Row 3
]
res = api.create_data_extension_rows_async("DE_Key", items_list)
res = api.upsert_data_extension_rows_async("DE_Key", items_list)

# Retrieve Data Extension Rows via REST API for more advanced parameters
items, items_count = api.get_data_extension_rows_rest(
    customer_key="DE_CUSTOMER_KEY",
    search_filter=complex_filter(
        simple_filter("first_name", Operator.EQUALS, "John"),
        'AND',
        simple_filter("last_name", Operator.EQUALS, "Doe")
    ),
    property_list=["email_address", "first_name", "last_name"],
    order_by="first_name ASC,last_name DESC",
    page_size=100,
    page=5
)

items, items_count = api.get_data_extension_rows_rest(
    customer_key="DE_CUSTOMER_KEY",
    search_filter=simple_filter("full_name", Operator.LIKE, "Jo%Doe"),
    property_list=["email_address", "full_name"],
    max_rows=300
)

# Get Email Rendered Preview
res = api.get_objects(
    ObjectType.EMAIL, 
    simple_filter("Name", Operator.EQUALS, "BCLA_202001_06-LIVE"),
    property_list=["ID"]
)
email_id = res.results[0].ID
res = api.get_email_preview(
    email_id,
    data_extension_key="My_DE_Key",
    contact_key="My_Contact_Key"
)
```

### Get More Results

```python
response = api.get_objects(ObjectType.LIST_SUBSCRIBER,
                           simple_filter("ListID", Operator.EQUALS, 1234),
                           property_list=["ID"])
total = len(response.results)
while response.more_results:
    response = api.get_more_results()
    total += len(response.results)
```

### Extract Request

```python
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()
response = api.extract_data(
    parameters={"AccountIDs": "123456", "_AsyncID": 0,
        "StartDate": start_date, "EndDate": end_date,
        "ExtractSent": "true", "ExtractSendJobs": "true", "ExtractBounces": "false", "ExtractClicks": "false",
        "ExtractOpens": "false", "ExtractUnsubs": "false", "ExtractConversions": "false",
        "IncludeTestSends": "false", "IncludeUniqueClicks": "false", "IncludeUniqueOpens": "false",
        "ExtractSurveyResponses": "false", "Format": "tab",
        "OutputFileName": "extract.zip"})
```

### Perform Request

You can Perform the list of actions found [here](https://help.marketingcloud.com/en/technical_library/web_service_guide/methods/perform/).

```python
response = api.get_objects(
    ObjectType.IMPORT_DEFINITION,
    simple_filter("Name", Operator.EQUALS, "Import_my_file")
)
try:
    import_def = response.results[0]
    response = api.perform_action("start", import_def)
except IndexError:
    print("No Import Definition found")
```

### List SOAP API Object Properties

```python
response = api.get_info(ObjectType.CONTENT_AREA)
```

## Responses

All methods on Fuel SDK objects return a generic object that follows the same structure, regardless of the type of call.  This object contains a common set of properties used to display details about the request.

| Parameter | Description                                                     |
| --------- | --------------------------------------------------------------- |
| status    | Boolean value that indicates if the call was successful         |
| code      | HTTP Error Code (will always be 200 for SOAP requests)          |
| message   | Text values containing more details in the event of an Error    |
| results   | Collection containing the details unique to the method called.  |

## Debug

To debug any issues, activate the debug mode:
```python
api = ET_API(debug=True)
```

## Requirements

Python 2.7.x
Python 3.x

Libraries:

* Salesforce-FuelSDK>=1.3.0
* PyJWT>=0.1.9
* requests>=2.18.4
* suds-jurko>=0.6
