#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import json
import subprocess


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
# Target ratio
target_ratio = require_resolutions[2]["ratio"]
horizontal_criteria_ratio = 16
vertical_criteria_ratio = 9

# Target duration(min)
duration_upper_limit = 45
duration_lower_limit = 35
duration_flag = True

# Target file size(MiB)
size_upper_limit = 1000
size_flag = False


def main():
    args = get_args()

    if args.input is not None:
        input = args.input[0]
        get_files = subprocess.Popen(
                ["ls", str(input)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

        media_status = []

        for filename in str(get_files.stdout.read().decode()).split("\n"):
            if len(filename) != 0:
                media_width, media_height, media_duration, media_size = _get_media_info(input, filename)
                media_status_dict = _create_media_status(media_width, media_height, media_duration, media_size, filename)

                media_status.append(media_status_dict)

    print(json.dumps(media_status))


def _get_media_info(input, filename):
    """
    Get Input media Information

    Args:
        input(str): filename including directory
        filename(str): filename
    Returns:
        media_width(int): media width(px)
        media_height(int): media height(px)
        media_duration(int): media duration(sec)
        media_size(int): media size(byte)
    """

    # Get information on videos under the specified folder
    get_proc_cmd = [
            'ffprobe',
            '-hide_banner',
            '-show_streams',
            '-show_format',
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
                '-show_format',
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
    media_duration = int(media_data['format']['duration'].split('.')[0])
    media_size = int(media_data['format']['size'])

    return media_width, media_height, media_duration, media_size


def _create_media_status(media_width, media_height, media_duration, media_size, filename):
    """
    Create information for each video

    Args:
        media_width(int): media width(px)
        media_height(int): media height(px)
        media_duration(int): media duration(sec)
        media_size(int): media size(byte)
        filename(str): filename
    Returns:
        media_status_dict(dict): media information
    """
    # Check resolution
    if media_width < require_resolutions[target_ratio]["width"] or \
            media_height < require_resolutions[target_ratio]["height"]:
        resolution_status = "NG"
    else:
        resolution_status = "OK"
    resolution_type = "NON STANDARD"

    # Check aspect ratio
    if media_width % horizontal_criteria_ratio == 0 and \
            media_height % vertical_criteria_ratio == 0 and \
            media_width // horizontal_criteria_ratio == media_height // vertical_criteria_ratio:
        aspect_status = "OK"
        aspect_ratio = "16:9"
    else:
        aspect_status = "NG"
        aspect_ratio = "{} x {}".format(media_width, media_height)

    # Check if the resolution is standard
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

    # Check duration(if True)
    if duration_flag:
        media_duration_min = media_duration // 60
        if media_duration_min < duration_lower_limit:
            duration_status = "NG"
            duration_description = "The media duration is shorter than {} minutes.".format(duration_lower_limit)
        elif duration_lower_limit <= media_duration_min <= duration_upper_limit:
            duration_status = "OK"
            duration_description = "Appropriate media duration."
        else:
            duration_status = "NG"
            duration_description = "The media duration is longer than {} minutes.".format(duration_upper_limit)
    else:
        duration_status = False

    # Check media size(if True)
    if size_flag:
        media_size_mib = media_size // (1024*1024)
        if media_size_mib >= size_upper_limit:
            size_status = "NG"
            size_description = "The media size exceeds {} MiB.".format(size_upper_limit)
        else:
            size_status = "OK"
            size_description = "Appropriate media size."
    else:
        size_status = False

    media_status_dict = {
        "file_name": filename,
        "resolution_status": resolution_status,
        "resolution_type": resolution_type,
        "aspect_status": aspect_status,
        "aspect_ratio": aspect_ratio
        }

    if duration_status:
        media_status_dict["duration_status"] = duration_status
        media_status_dict["duration_description"] = duration_description
    if size_status:
        media_status_dict["size_status"] = size_status
        media_status_dict["size_description"] = size_description

    return media_status_dict


def get_args():
    parser = argparse.ArgumentParser(description="""
    Get media information and determine if the criteria are met.
    """)

    parser.add_argument('--input',
                        nargs=1,
                        type=str,
                        required=True,
                        metavar='INPUT',
                        help='File or folder to be analyzed.')

    parser.add_argument('--s3',
                        action='store_true',
                        help='Determine whether to send to S3.')

    return parser.parse_args()


if __name__ == "__main__":
    main()
