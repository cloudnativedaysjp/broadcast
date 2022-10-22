<a name="__pageTop"></a>
# openapi_client.apis.tags.event_api.EventApi

All URIs are relative to *http://localhost:8080*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_events_event_abbr_get**](#api_v1_events_event_abbr_get) | **get** /api/v1/events/{eventAbbr} | 
[**api_v1_events_get**](#api_v1_events_get) | **get** /api/v1/events | 

# **api_v1_events_event_abbr_get**
<a name="api_v1_events_event_abbr_get"></a>
> Event api_v1_events_event_abbr_get(event_abbr)



### Example

```python
import openapi_client
from openapi_client.apis.tags import event_api
from openapi_client.model.event import Event
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8080
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8080"
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = event_api.EventApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'eventAbbr': "eventAbbr_example",
    }
    try:
        api_response = api_instance.api_v1_events_event_abbr_get(
            path_params=path_params,
        )
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling EventApi->api_v1_events_event_abbr_get: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
eventAbbr | EventAbbrSchema | | 

# EventAbbrSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#api_v1_events_event_abbr_get.ApiResponseFor200) | OK
400 | [ApiResponseFor400](#api_v1_events_event_abbr_get.ApiResponseFor400) | Invalid [eventAbbr] supplied
404 | [ApiResponseFor404](#api_v1_events_event_abbr_get.ApiResponseFor404) | Event not found

#### api_v1_events_event_abbr_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Event**](../../models/Event.md) |  | 


#### api_v1_events_event_abbr_get.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### api_v1_events_event_abbr_get.ApiResponseFor404
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **api_v1_events_get**
<a name="api_v1_events_get"></a>
> [Event] api_v1_events_get()



### Example

```python
import openapi_client
from openapi_client.apis.tags import event_api
from openapi_client.model.event import Event
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8080
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8080"
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = event_api.EventApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        api_response = api_instance.api_v1_events_get()
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling EventApi->api_v1_events_get: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#api_v1_events_get.ApiResponseFor200) | OK
400 | [ApiResponseFor400](#api_v1_events_get.ApiResponseFor400) | Invalid [eventAbbr] supplied
404 | [ApiResponseFor404](#api_v1_events_get.ApiResponseFor404) | Event not found

#### api_v1_events_get.ApiResponseFor200
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
[**Event**]({{complexTypePrefix}}Event.md) | [**Event**]({{complexTypePrefix}}Event.md) | [**Event**]({{complexTypePrefix}}Event.md) |  | 

#### api_v1_events_get.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### api_v1_events_get.ApiResponseFor404
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

