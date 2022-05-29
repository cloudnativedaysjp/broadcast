#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import subprocess
import sys


require_resolutions = [
        {
            "ratio": 0,
            "type": "SD",
            "width": 720,
            "height": 480
        },
        {
            "ratio": 1,
            "type": "HD",
            "width": 1280,
            "height": 720
        },
        {
            "ratio": 2,
            "type": "FullHD",
            "width": 1920,
            "height": 1080
        },
        {
            "ratio": 3,
            "type": "WQHD",
            "width": 2560,
            "height": 1440
        },
        {
            "ratio": 4,
            "type": "4K",
            "width": 4096,
            "height": 2160
        }
    ]

# Default criterion
target_ratio = require_resolutions[2]["ratio"]
horizontal_criteria_ratio = 16
vertical_criteria_ratio = 9


def get_media_info(input, filename):
    """
    Get Input media Information

    Args:
        input(str): filename including directory
        filename(str): filename
    Returns:
        media_width(int): media width(px)
        media_height(int): media height(px)
    """

    # Get information on videos under the specified folder
    get_proc_cmd = [
            'ffprobe',
            '-hide_banner',
            '-show_streams',
            '-of',
            'json',
            str(input)+"/" + str(filename)
        ]
    proc_mediainfo = subprocess.run(
            get_proc_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    media_data = json.loads(proc_mediainfo.stdout)

    # Get information on video about the specified file
    if len(media_data) == 0:
        get_proc_cmd = [
                'ffprobe',
                '-hide_banner',
                '-show_streams',
                '-of',
                'json',
                str(input)
            ]
        proc_mediainfo = subprocess.run(
                get_proc_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        media_data = json.loads(proc_mediainfo.stdout)

    media_width = media_data['streams'][0]['width']
    media_height = media_data['streams'][0]['height']

    return media_width, media_height


def create_media_status(media_width, media_height, filename):
    """
    Create information for each video

    Args:
        media_width(int): media width(px)
        media_height(int): media height(px)
        filename(str): filename
    Returns:
        media_status_dict(dict): media information
    """
    if media_width < require_resolutions[target_ratio]["width"] or \
            media_height < require_resolutions[target_ratio]["height"]:
        resolution_status = "NG"
    else:
        resolution_status = "OK"
    resolution_type = "NON STANDARD"

    if media_width % horizontal_criteria_ratio == 0 and \
            media_height % vertical_criteria_ratio == 0 and\
            media_width // horizontal_criteria_ratio == media_height // vertical_criteria_ratio:
        aspect_status = "OK"
        aspect_ratio = "16:9"
    else:
        aspect_status = "NG"
        aspect_ratio = "{} x {}".format(media_width, media_height)

    for resolution_definition in require_resolutions:
        # check if standard
        if media_width == resolution_definition["width"] and\
                media_height == resolution_definition["height"]:
            set_ratio = resolution_definition["ratio"]
            if set_ratio == target_ratio:
                resolution_status = "OK"
            elif set_ratio != target_ratio:
                resolution_status = "NG"
            resolution_type = resolution_definition["type"]

            if media_width % 16 == 0 and media_height % 9 == 0:
                aspect_status = "OK"
                aspect_ratio = "16:9"
            else:
                aspect_status = "NG"
                aspect_ratio = "{} x {}".format(media_width, media_height)

    media_status_dict = {
        "file_name": filename,
        "resolution_status": resolution_status,
        "resolution_type": resolution_type,
        "aspect_status": aspect_status,
        "aspect_ratio": aspect_ratio
        }

    return media_status_dict


def main():
    args = sys.argv
    input = args[1]

    get_files = subprocess.Popen(
            ["ls", str(input)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    media_status = []

    for filename in str(get_files.stdout.read().decode()).split("\n"):
        if len(filename) != 0:
            media_width, media_height = get_media_info(input, filename)
            media_status_dict = create_media_status(media_width, media_height, filename)

            media_status.append(media_status_dict)

    print(json.dumps(media_status))


if __name__ == "__main__":
    main()
