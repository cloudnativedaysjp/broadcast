# coding: utf-8

# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from openapi_client.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from openapi_client.model.booth import Booth
from openapi_client.model.chat_message import ChatMessage
from openapi_client.model.chat_message_properties import ChatMessageProperties
from openapi_client.model.event import Event
from openapi_client.model.profile import Profile
from openapi_client.model.sponsor import Sponsor
from openapi_client.model.talk import Talk
from openapi_client.model.track import Track
from openapi_client.model.update_chat_message import UpdateChatMessage
from openapi_client.model.video_registration import VideoRegistration
from openapi_client.model.viewer_count import ViewerCount
