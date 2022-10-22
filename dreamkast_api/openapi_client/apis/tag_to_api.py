import typing_extensions

from openapi_client.apis.tags import TagValues
from openapi_client.apis.tags.booth_api import BoothApi
from openapi_client.apis.tags.chat_message_api import ChatMessageApi
from openapi_client.apis.tags.event_api import EventApi
from openapi_client.apis.tags.profile_api import ProfileApi
from openapi_client.apis.tags.sponsor_api import SponsorApi
from openapi_client.apis.tags.talk_api import TalkApi
from openapi_client.apis.tags.track_api import TrackApi
from openapi_client.apis.tags.video_registration_api import VideoRegistrationApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.BOOTH: BoothApi,
        TagValues.CHAT_MESSAGE: ChatMessageApi,
        TagValues.EVENT: EventApi,
        TagValues.PROFILE: ProfileApi,
        TagValues.SPONSOR: SponsorApi,
        TagValues.TALK: TalkApi,
        TagValues.TRACK: TrackApi,
        TagValues.VIDEO_REGISTRATION: VideoRegistrationApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.BOOTH: BoothApi,
        TagValues.CHAT_MESSAGE: ChatMessageApi,
        TagValues.EVENT: EventApi,
        TagValues.PROFILE: ProfileApi,
        TagValues.SPONSOR: SponsorApi,
        TagValues.TALK: TalkApi,
        TagValues.TRACK: TrackApi,
        TagValues.VIDEO_REGISTRATION: VideoRegistrationApi,
    }
)
