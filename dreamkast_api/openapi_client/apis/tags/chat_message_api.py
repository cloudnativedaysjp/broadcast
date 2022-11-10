# coding: utf-8

"""
    Dreamkast API

    This is a API definition of the Dreamakst. You can find a documentation of this API at http://api-docs.dev.cloudnativedays.jp/.  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""

from openapi_client.paths.api_v1_chat_messages.get import ApiV1ChatMessagesGet
from openapi_client.paths.api_v1_chat_messages_message_id.put import ApiV1ChatMessagesMessageIdPut
from openapi_client.paths.api_v1_chat_messages.post import ApiV1ChatMessagesPost


class ChatMessageApi(
    ApiV1ChatMessagesGet,
    ApiV1ChatMessagesMessageIdPut,
    ApiV1ChatMessagesPost,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass