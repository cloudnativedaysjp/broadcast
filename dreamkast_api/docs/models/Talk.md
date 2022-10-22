# openapi_client.model.talk.Talk

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**trackId** | decimal.Decimal, int, float,  | decimal.Decimal,  |  | 
**videoId** | str,  | str,  |  | 
**abstract** | str,  | str,  |  | 
**talkDifficulty** | str,  | str,  |  | 
**title** | str,  | str,  |  | 
**talkCategory** | str,  | str,  |  | 
**showOnTimetable** | bool,  | BoolClass,  |  | 
**[speakers](#speakers)** | list, tuple,  | tuple,  | array of speakers name | 
**dayId** | None, decimal.Decimal, int, float,  | NoneClass, decimal.Decimal,  |  | 
**startTime** | str,  | str,  |  | 
**endTime** | str,  | str,  |  | 
**id** | decimal.Decimal, int, float,  | decimal.Decimal,  |  | 
**talkDuration** | decimal.Decimal, int, float,  | decimal.Decimal,  |  | 
**conferenceId** | decimal.Decimal, int, float,  | decimal.Decimal,  |  | [optional] 
**videoPlatform** | str,  | str,  |  | [optional] 
**onAir** | bool,  | BoolClass,  |  | [optional] 
**documentUrl** | str,  | str,  |  | [optional] 
**conferenceDayId** | None, decimal.Decimal, int, float,  | NoneClass, decimal.Decimal,  |  | [optional] 
**conferenceDayDate** | None, str, date,  | NoneClass, str,  |  | [optional] value must conform to RFC-3339 full-date YYYY-MM-DD
**startOffset** | decimal.Decimal, int, float,  | decimal.Decimal,  |  | [optional] 
**endOffset** | decimal.Decimal, int, float,  | decimal.Decimal,  |  | [optional] 
**actualStartTime** | str,  | str,  |  | [optional] 
**actualEndTime** | str,  | str,  |  | [optional] 
**presentationMethod** | None, str,  | NoneClass, str,  |  | [optional] 

# speakers

array of speakers name

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | array of speakers name | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[items](#items) | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

# items

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | decimal.Decimal, int, float,  | decimal.Decimal,  |  | [optional] 
**name** | str,  | str,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

