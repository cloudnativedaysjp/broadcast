# coding: utf-8

"""
    Dreamkast API

    This is a API definition of the Dreamakst. You can find a documentation of this API at http://api-docs.dev.cloudnativedays.jp/.  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""

from openapi_client.paths.api_v1_tracks.get import ApiV1TracksGet
from openapi_client.paths.api_v1_tracks_track_id.get import ApiV1TracksTrackIdGet
from openapi_client.paths.api_v1_tracks_track_id_viewer_count.get import ApiV1TracksTrackIdViewerCountGet


class TrackApi(
    ApiV1TracksGet,
    ApiV1TracksTrackIdGet,
    ApiV1TracksTrackIdViewerCountGet,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass