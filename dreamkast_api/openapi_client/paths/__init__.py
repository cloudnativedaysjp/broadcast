# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from openapi_client.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    API_V1_EVENT_ABBR_MY_PROFILE = "/api/v1/{eventAbbr}/my_profile"
    API_V1_EVENTS = "/api/v1/events"
    API_V1_EVENTS_EVENT_ABBR = "/api/v1/events/{eventAbbr}"
    API_V1_TRACKS = "/api/v1/tracks"
    API_V1_TRACKS_TRACK_ID = "/api/v1/tracks/{trackId}"
    API_V1_TRACKS_TRACK_ID_VIEWER_COUNT = "/api/v1/tracks/{trackId}/viewer_count"
    API_V1_TALKS = "/api/v1/talks"
    API_V1_TALKS_TALK_ID = "/api/v1/talks/{talkId}"
    API_V1_TALKS_TALK_ID_VIDEO_REGISTRATION = "/api/v1/talks/{talkId}/video_registration"
    API_V1_CHAT_MESSAGES = "/api/v1/chat_messages"
    API_V1_CHAT_MESSAGES_MESSAGE_ID = "/api/v1/chat_messages/{messageId}"
    API_V1_SPONSORS = "/api/v1/sponsors"
    API_V1_BOOTHS_BOOTH_ID = "/api/v1/booths/{boothId}"
