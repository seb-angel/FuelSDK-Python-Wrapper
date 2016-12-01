# FuelSDK-Python-Wrapper
Simplify and improve the FuelSDK for Salesforce Marketing Cloud (ExactTarget).

## Overview
The Fuel SDK Wrapper for Python add functionalities to the default Fuel SDK and provides access to more SOAP API objects. The Fuel SDK documentation can be found [here](https://github.com/salesforce-marketingcloud/FuelSDK-Python).

## Installation
```
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
```
params = {
    "clientid": "YOUR_CLIENT_ID",
    "clientsecret": "YOUR_CLIENT_SECRET"
}
api = ET_API(params=params)
```

## Example Request

### Get the List objects

```python
# Add a require statement to reference the Fuel SDK's functionality:
from FuelSDKWrapper import ET_API, ObjectType

# Next, create an instance of the ET_API class:
api = ET_API()

# Get the List objects:
response = api.get_objects(ObjectType.LIST)

# Print out the results for viewing
print('Post Status: {}'.format(response.status))
print('Code: {}'.format(response.code))
print('Message: {}'.format(response.message))
print('Result Count: {}'.format(len(response.results)))
print('Results: {}'.format(response.results))
```

### Some examples of utilization

```
from FuelSDKWrapper import ET_API, ObjectType, Operator, search_filter
from datetime import datetime, timedelta

api = ET_API()

response = api.get_objects(
    ObjectType.SUBSCRIBER,
    search_filter("EmailAddress", Operator.EQUALS, "my.email@domain.com")
)

response = api.get_objects(
    ObjectType.FOLDER,
    search_filter("Name", Operator.EQUALS, "My_Folder"),
    property_list=["ID", "Name"]
)

dt = datetime.now() - timedelta(days=30)
response = api.get_objects(
    ObjectType.SEND,
    search_filter("SendDate", Operator.GREATER_THAN, dt)
)
```

### Get More Results

```
api = ET_API()

response = api.get_objects(ObjectType.SUBSCRIBER)
i = 0
while len(response.results) > 0 and (i == 0 or response.more_results):
    if i > 0 and response.more_results:
        res = api.continue_request(response.request_id)
        
    for subscriber in response.results:
        print("Subscriber: {}".format(subscriber))
```

### Perform Request

You can Perform the list of actions found [here](https://help.marketingcloud.com/en/technical_library/web_service_guide/methods/perform/).

```
api = ET_API()

response = api.get_objects(
    ObjectType.IMPORT_DEFINITION,
    search_filter("Name", Operator.EQUALS, "Import_my_file")
)
try:
    import_def = response.results[0]
    response = api.perform_action("start", import_def)
except IndexError:
    pass
```

### List SOAP API Object Properties

```
api = ET_API()

response = api.get_info(ObjectType.CONTENT_AREA)
```

### Object Type Missing

In case the Object Type is missing from the ObjectType class, you can use a string directly: 
```
api = ET_API()

response = api.get_objects("AccountUser")
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
```
api = ET_API(debug=True)
```

## Requirements

Python 2.7.x

Libraries:

* FuelSDK>=0.9.3
* PyJWT>=0.1.9
* requests>=2.2.1
* suds>=0.4
* suds-jurko>=0.6
