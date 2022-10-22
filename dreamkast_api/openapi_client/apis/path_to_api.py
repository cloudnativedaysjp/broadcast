import typing_extensions

from openapi_client.paths import PathValues
from openapi_client.apis.paths.api_v1_event_abbr_my_profile import ApiV1EventAbbrMyProfile
from openapi_client.apis.paths.api_v1_events import ApiV1Events
from openapi_client.apis.paths.api_v1_events_event_abbr import ApiV1EventsEventAbbr
from openapi_client.apis.paths.api_v1_tracks import ApiV1Tracks
from openapi_client.apis.paths.api_v1_tracks_track_id import ApiV1TracksTrackId
from openapi_client.apis.paths.api_v1_tracks_track_id_viewer_count import ApiV1TracksTrackIdViewerCount
from openapi_client.apis.paths.api_v1_talks import ApiV1Talks
from openapi_client.apis.paths.api_v1_talks_talk_id import ApiV1TalksTalkId
from openapi_client.apis.paths.api_v1_talks_talk_id_video_registration import ApiV1TalksTalkIdVideoRegistration
from openapi_client.apis.paths.api_v1_chat_messages import ApiV1ChatMessages
from openapi_client.apis.paths.api_v1_chat_messages_message_id import ApiV1ChatMessagesMessageId
from openapi_client.apis.paths.api_v1_sponsors import ApiV1Sponsors
from openapi_client.apis.paths.api_v1_booths_booth_id import ApiV1BoothsBoothId

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.API_V1_EVENT_ABBR_MY_PROFILE: ApiV1EventAbbrMyProfile,
        PathValues.API_V1_EVENTS: ApiV1Events,
        PathValues.API_V1_EVENTS_EVENT_ABBR: ApiV1EventsEventAbbr,
        PathValues.API_V1_TRACKS: ApiV1Tracks,
        PathValues.API_V1_TRACKS_TRACK_ID: ApiV1TracksTrackId,
        PathValues.API_V1_TRACKS_TRACK_ID_VIEWER_COUNT: ApiV1TracksTrackIdViewerCount,
        PathValues.API_V1_TALKS: ApiV1Talks,
        PathValues.API_V1_TALKS_TALK_ID: ApiV1TalksTalkId,
        PathValues.API_V1_TALKS_TALK_ID_VIDEO_REGISTRATION: ApiV1TalksTalkIdVideoRegistration,
        PathValues.API_V1_CHAT_MESSAGES: ApiV1ChatMessages,
        PathValues.API_V1_CHAT_MESSAGES_MESSAGE_ID: ApiV1ChatMessagesMessageId,
        PathValues.API_V1_SPONSORS: ApiV1Sponsors,
        PathValues.API_V1_BOOTHS_BOOTH_ID: ApiV1BoothsBoothId,
    }
)

path_to_api = PathToApi(
    {
        PathValues.API_V1_EVENT_ABBR_MY_PROFILE: ApiV1EventAbbrMyProfile,
        PathValues.API_V1_EVENTS: ApiV1Events,
        PathValues.API_V1_EVENTS_EVENT_ABBR: ApiV1EventsEventAbbr,
        PathValues.API_V1_TRACKS: ApiV1Tracks,
        PathValues.API_V1_TRACKS_TRACK_ID: ApiV1TracksTrackId,
        PathValues.API_V1_TRACKS_TRACK_ID_VIEWER_COUNT: ApiV1TracksTrackIdViewerCount,
        PathValues.API_V1_TALKS: ApiV1Talks,
        PathValues.API_V1_TALKS_TALK_ID: ApiV1TalksTalkId,
        PathValues.API_V1_TALKS_TALK_ID_VIDEO_REGISTRATION: ApiV1TalksTalkIdVideoRegistration,
        PathValues.API_V1_CHAT_MESSAGES: ApiV1ChatMessages,
        PathValues.API_V1_CHAT_MESSAGES_MESSAGE_ID: ApiV1ChatMessagesMessageId,
        PathValues.API_V1_SPONSORS: ApiV1Sponsors,
        PathValues.API_V1_BOOTHS_BOOTH_ID: ApiV1BoothsBoothId,
    }
)
