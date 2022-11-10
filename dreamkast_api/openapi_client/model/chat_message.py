# coding: utf-8

"""
    Dreamkast API

    This is a API definition of the Dreamakst. You can find a documentation of this API at http://api-docs.dev.cloudnativedays.jp/.  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from openapi_client import schemas  # noqa: F401


class ChatMessage(
    schemas.ComposedBase,
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "messageType",
            "body",
            "roomId",
        }
        additional_properties = schemas.NotAnyTypeSchema
        
        @classmethod
        @functools.lru_cache()
        def all_of(cls):
            # we need this here to make our import statements work
            # we must store _composed_schemas in here so the code is only run
            # when we invoke this method. If we kept this at the class
            # level we would get an error because the class level
            # code would be run when this module is imported, and these composed
            # classes don't exist yet because their module has not finished
            # loading
            return [
                ChatMessageProperties,
            ]

    
    
    def __getitem__(self, name: typing.Union[]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    def get_item_oapg(self, name: typing.Union[]):
        return super().get_item_oapg(name)

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
    ) -> 'ChatMessage':
        return super().__new__(
            cls,
            *args,
            _configuration=_configuration,
        )

from openapi_client.model.chat_message_properties import ChatMessageProperties