<a name="__pageTop"></a>
# openapi_client.apis.tags.chat_message_api.ChatMessageApi

All URIs are relative to *http://localhost:8080*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_chat_messages_get**](#api_v1_chat_messages_get) | **get** /api/v1/chat_messages | 
[**api_v1_chat_messages_message_id_put**](#api_v1_chat_messages_message_id_put) | **put** /api/v1/chat_messages/{messageId} | Update Chat Message
[**api_v1_chat_messages_post**](#api_v1_chat_messages_post) | **post** /api/v1/chat_messages | Post Chat Message

# **api_v1_chat_messages_get**
<a name="api_v1_chat_messages_get"></a>
> [ChatMessage] api_v1_chat_messages_get(event_abbrroom_idroom_type)



### Example

```python
import openapi_client
from openapi_client.apis.tags import chat_message_api
from openapi_client.model.chat_message import ChatMessage
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8080
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8080"
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = chat_message_api.ChatMessageApi(api_client)

    # example passing only required values which don't have defaults set
    query_params = {
        'eventAbbr': "eventAbbr_example",
        'roomId': "roomId_example",
        'roomType': "roomType_example",
    }
    try:
        api_response = api_instance.api_v1_chat_messages_get(
            query_params=query_params,
        )
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling ChatMessageApi->api_v1_chat_messages_get: %s\n" % e)

    # example passing only optional values
    query_params = {
        'eventAbbr': "eventAbbr_example",
        'roomId': "roomId_example",
        'roomType': "roomType_example",
        'createdFrom': "1970-01-01T00:00:00.00Z",
    }
    try:
        api_response = api_instance.api_v1_chat_messages_get(
            query_params=query_params,
        )
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling ChatMessageApi->api_v1_chat_messages_get: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
eventAbbr | EventAbbrSchema | | 
roomId | RoomIdSchema | | 
roomType | RoomTypeSchema | | 
createdFrom | CreatedFromSchema | | optional


# EventAbbrSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# RoomIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# RoomTypeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# CreatedFromSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str, datetime,  | str,  |  | value must conform to RFC-3339 date-time

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#api_v1_chat_messages_get.ApiResponseFor200) | OK
400 | [ApiResponseFor400](#api_v1_chat_messages_get.ApiResponseFor400) | Invalid params supplied
404 | [ApiResponseFor404](#api_v1_chat_messages_get.ApiResponseFor404) | ChatMessage not found

#### api_v1_chat_messages_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**ChatMessage**]({{complexTypePrefix}}ChatMessage.md) | [**ChatMessage**]({{complexTypePrefix}}ChatMessage.md) | [**ChatMessage**]({{complexTypePrefix}}ChatMessage.md) |  | 

#### api_v1_chat_messages_get.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### api_v1_chat_messages_get.ApiResponseFor404
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **api_v1_chat_messages_message_id_put**
<a name="api_v1_chat_messages_message_id_put"></a>
> [ChatMessage] api_v1_chat_messages_message_id_put(message_id)

Update Chat Message

### Example

```python
import openapi_client
from openapi_client.apis.tags import chat_message_api
from openapi_client.model.chat_message import ChatMessage
from openapi_client.model.update_chat_message import UpdateChatMessage
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8080
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8080"
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = chat_message_api.ChatMessageApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'messageId': "messageId_example",
    }
    try:
        # Update Chat Message
        api_response = api_instance.api_v1_chat_messages_message_id_put(
            path_params=path_params,
        )
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling ChatMessageApi->api_v1_chat_messages_message_id_put: %s\n" % e)

    # example passing only optional values
    path_params = {
        'messageId': "messageId_example",
    }
    body = UpdateChatMessage()
    try:
        # Update Chat Message
        api_response = api_instance.api_v1_chat_messages_message_id_put(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling ChatMessageApi->api_v1_chat_messages_message_id_put: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, Unset] | optional, default is unset |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**UpdateChatMessage**](../../models/UpdateChatMessage.md) |  | 


### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
messageId | MessageIdSchema | | 

# MessageIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#api_v1_chat_messages_message_id_put.ApiResponseFor200) | OK
403 | [ApiResponseFor403](#api_v1_chat_messages_message_id_put.ApiResponseFor403) | Don&#x27;t have permission to update
400 | [ApiResponseFor400](#api_v1_chat_messages_message_id_put.ApiResponseFor400) | Invalid params supplied
404 | [ApiResponseFor404](#api_v1_chat_messages_message_id_put.ApiResponseFor404) | ChatMessage not found

#### api_v1_chat_messages_message_id_put.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**ChatMessage**]({{complexTypePrefix}}ChatMessage.md) | [**ChatMessage**]({{complexTypePrefix}}ChatMessage.md) | [**ChatMessage**]({{complexTypePrefix}}ChatMessage.md) |  | 

#### api_v1_chat_messages_message_id_put.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor403ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor403ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**error** | str,  | str,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

#### api_v1_chat_messages_message_id_put.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### api_v1_chat_messages_message_id_put.ApiResponseFor404
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **api_v1_chat_messages_post**
<a name="api_v1_chat_messages_post"></a>
> api_v1_chat_messages_post()

Post Chat Message

### Example

```python
import openapi_client
from openapi_client.apis.tags import chat_message_api
from openapi_client.model.chat_message import ChatMessage
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8080
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8080"
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = chat_message_api.ChatMessageApi(api_client)

    # example passing only optional values
    body = ChatMessage()
    try:
        # Post Chat Message
        api_response = api_instance.api_v1_chat_messages_post(
            body=body,
        )
    except openapi_client.ApiException as e:
        print("Exception when calling ChatMessageApi->api_v1_chat_messages_post: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, Unset] | optional, default is unset |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ChatMessage**](../../models/ChatMessage.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#api_v1_chat_messages_post.ApiResponseFor201) | CREATED

#### api_v1_chat_messages_post.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

