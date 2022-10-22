<a name="__pageTop"></a>
# openapi_client.apis.tags.video_registration_api.VideoRegistrationApi

All URIs are relative to *http://localhost:8080*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_talks_talk_id_video_registration_get**](#api_v1_talks_talk_id_video_registration_get) | **get** /api/v1/talks/{talkId}/video_registration | 
[**api_v1_talks_talk_id_video_registration_put**](#api_v1_talks_talk_id_video_registration_put) | **put** /api/v1/talks/{talkId}/video_registration | Put VideoRegistration

# **api_v1_talks_talk_id_video_registration_get**
<a name="api_v1_talks_talk_id_video_registration_get"></a>
> VideoRegistration api_v1_talks_talk_id_video_registration_get(talk_id)



### Example

```python
import openapi_client
from openapi_client.apis.tags import video_registration_api
from openapi_client.model.video_registration import VideoRegistration
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8080
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8080"
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = video_registration_api.VideoRegistrationApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'talkId': "talkId_example",
    }
    try:
        api_response = api_instance.api_v1_talks_talk_id_video_registration_get(
            path_params=path_params,
        )
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling VideoRegistrationApi->api_v1_talks_talk_id_video_registration_get: %s\n" % e)
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
talkId | TalkIdSchema | | 

# TalkIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#api_v1_talks_talk_id_video_registration_get.ApiResponseFor200) | OK
400 | [ApiResponseFor400](#api_v1_talks_talk_id_video_registration_get.ApiResponseFor400) | Invalid params supplied
401 | [ApiResponseFor401](#api_v1_talks_talk_id_video_registration_get.ApiResponseFor401) | Unauthorized
404 | [ApiResponseFor404](#api_v1_talks_talk_id_video_registration_get.ApiResponseFor404) | Talk not found

#### api_v1_talks_talk_id_video_registration_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**VideoRegistration**](../../models/VideoRegistration.md) |  | 


#### api_v1_talks_talk_id_video_registration_get.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### api_v1_talks_talk_id_video_registration_get.ApiResponseFor401
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### api_v1_talks_talk_id_video_registration_get.ApiResponseFor404
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **api_v1_talks_talk_id_video_registration_put**
<a name="api_v1_talks_talk_id_video_registration_put"></a>
> api_v1_talks_talk_id_video_registration_put(talk_id)

Put VideoRegistration

### Example

```python
import openapi_client
from openapi_client.apis.tags import video_registration_api
from openapi_client.model.video_registration import VideoRegistration
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8080
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8080"
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = video_registration_api.VideoRegistrationApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'talkId': "talkId_example",
    }
    try:
        # Put VideoRegistration
        api_response = api_instance.api_v1_talks_talk_id_video_registration_put(
            path_params=path_params,
        )
    except openapi_client.ApiException as e:
        print("Exception when calling VideoRegistrationApi->api_v1_talks_talk_id_video_registration_put: %s\n" % e)

    # example passing only optional values
    path_params = {
        'talkId': "talkId_example",
    }
    body = VideoRegistration(
        url="url_example",
        status="unsubmitted",
        statistics=dict(),
        created_at="created_at_example",
        updated_at="updated_at_example",
    )
    try:
        # Put VideoRegistration
        api_response = api_instance.api_v1_talks_talk_id_video_registration_put(
            path_params=path_params,
            body=body,
        )
    except openapi_client.ApiException as e:
        print("Exception when calling VideoRegistrationApi->api_v1_talks_talk_id_video_registration_put: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, Unset] | optional, default is unset |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**VideoRegistration**](../../models/VideoRegistration.md) |  | 


### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
talkId | TalkIdSchema | | 

# TalkIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#api_v1_talks_talk_id_video_registration_put.ApiResponseFor200) | OK
400 | [ApiResponseFor400](#api_v1_talks_talk_id_video_registration_put.ApiResponseFor400) | Invalid params supplied
401 | [ApiResponseFor401](#api_v1_talks_talk_id_video_registration_put.ApiResponseFor401) | Unauthorized
404 | [ApiResponseFor404](#api_v1_talks_talk_id_video_registration_put.ApiResponseFor404) | Talk not found

#### api_v1_talks_talk_id_video_registration_put.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### api_v1_talks_talk_id_video_registration_put.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### api_v1_talks_talk_id_video_registration_put.ApiResponseFor401
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### api_v1_talks_talk_id_video_registration_put.ApiResponseFor404
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

