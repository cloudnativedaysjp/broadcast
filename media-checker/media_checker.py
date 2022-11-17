#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
from collections import OrderedDict
import csv
import datetime
import glob
import json
import jwt
import subprocess
import os
import shutil
import sys
import urllib.request
import urllib.error
import pytz

# 要求解像度定義
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

# デフォルトの解像度判定基準
lower_target_ratio = require_resolutions[1]["ratio"]
upper_target_ratio = require_resolutions[2]["ratio"]
horizontal_criteria_ratio = 16
vertical_criteria_ratio = 9

# デフォルトのファイルサイズ(MB)判定基準
size_upper_limit = 2000
size_flag = False


def main():
    args = get_args()

    args.handler(args)


def command_put(args):
    # 変数読み込み
    json_open = open('./media_checker_env.json', 'r')
    json_load = json.load(json_open)

    # Dk API tokenの有効期限を確認し、期限切れの場合は更新する
    if not _dk_token_check(json_load['TOKEN']):
        _dk_token_update(json_load['AUTH0_DOMAIN'], json_load['AUDIENCE'], json_load['CLIENT_ID'], json_load['CLIENT_SECRET'])

    # Dk連携用の変数がセットできていることを確認する
    # 環境変数($TOKEN/$DREAMKAST_DOMAIN)の確認
    if json_load['TOKEN'] is None or \
            json_load['DREAMKAST_DOMAIN'] is None:
        # 環境変数の存在が確認できない場合、その旨をSlack通知し処理を終了する
        message = "`subject`: $TOKEN or $DREAMKAST_DOMAIN" + '\r\n' +\
                  "`reason`: 環境変数の読み込みに失敗しました"
        _send_errlog_to_slack(message, json_load['SLACKURL'])
        sys.exit(1)

    # 動画が格納されているフォルダの第一階層のフォルダ名を取得する
    input_dir = json_load['GROUPFOLDER_PATH'] + json_load['GLOUPFOLDER_ID']

    # CSVファイルを読み込んで、セッション単位で最新のファイルを特定する
    # CSVファイルの中身をlist形式で取得
    csv_file = open("".join(args.csv),
                    "r",
                    encoding="utf_8",
                    errors="",
                    newline="")

    list_csv_file = csv.reader(csv_file,
                               delimiter=",",
                               doublequote=True,
                               lineterminator="\r\n",
                               quotechar='"',
                               skipinitialspace=True)

    # CSVを一行ずつ判定し、セッション番号からはじまるフォルダがあれば後続処理、なければcontinue
    header = next(list_csv_file)

    duration_upper_limit = int("".join(args.upper_limit))
    duration_lower_limit = int("".join(args.lower_limit))

    list_of_dirs = glob.glob("".join(input_dir) + '/*')
    for row in list_csv_file:
        for dirs in list_of_dirs:
            directory = dirs.split('/')[-1]
            if directory.split('_')[0] == row[0]:
                list_of_files = glob.glob("".join(input_dir) + '/' + row[0] + '*' + '/*.mp4')
                list_of_files.extend(glob.glob("".join(input_dir) + '/' + row[0] + '*' + '/*.mov'))
                # フォルダ内の最新のファイルをフルパスで取得する
                try:
                    latest_file = max(list_of_files, key=os.path.getctime)
                except ValueError:
                    continue

                # .part がファイル名の末尾に付与されている場合は処理をスキップする
                if latest_file.split('.')[-1] == "part":
                    continue

                # 最新ファイルの動画情報を生成する
                try:
                    media_width, media_height, media_duration, media_size = _get_media_info(latest_file)
                except (KeyError, UnboundLocalError):
                    # 動画情報の取得に失敗した場合にSlack通知
                    import traceback
                    message = "`subject`: " + latest_file + '\r\n' +\
                              "`reason`: 動画情報の取得に失敗しました" + '\r\n' +\
                              "`error detail`: " + '\r\n' +\
                              "```" + '\r\n' +\
                              traceback.format_exc() +\
                              "```"
                    _send_errlog_to_slack(message, json_load['SLACKURL'])
                    continue

                filename = row[1] + ".mp4"
                media_status_dict = _create_media_status(media_width,
                                                         media_height,
                                                         media_duration,
                                                         media_size,
                                                         duration_upper_limit,
                                                         duration_lower_limit,
                                                         filename)

                # DkにAPI経由で動画情報を送る
                talkid = row[0]
                url = 'https://' + json_load['DREAMKAST_DOMAIN'] + '/api/v1/talks/' + talkid + '/video_registration'
                header = {'Authorization': 'Bearer ' + json_load['TOKEN']}
                put_data = json.dumps(media_status_dict, ensure_ascii=False)

                dk_req = urllib.request.Request(url,
                                                headers=header,
                                                data=put_data.encode(),
                                                method='PUT')

                try:
                    urllib.request.urlopen(dk_req)
                except:
                    # Dk連携が失敗した場合にSlack通知
                    import traceback
                    message = "`subject`: " + filename + '\r\n' +\
                              "`reason`: Dk連携に失敗しました" + '\r\n' +\
                              "`error detail`: " + '\r\n' +\
                              "```" + '\r\n' +\
                              traceback.format_exc() +\
                              "```"
                    _send_errlog_to_slack(message, json_load['SLACKURL'])
                    sys.exit(1)

                # Dk連携が完了後、動画をRename
                oldpath = latest_file
                newpath_filename = row[0]
                # volmod_filename = row[1].replace('/', '_')
                newpath = input_dir + "/" + directory + "/" + newpath_filename + ".mp4"
                # newpath_volmod = input_dir + "/" + directory + "/" + volmod_filename + "_mod.mp4"

                # 動画音量の規格化を行う(新旧ファイルを保持)
                max_vol = _check_volume(latest_file)
                if max_vol.split("-")[-1] != "0.0":
                    _volume_converter(max_vol, oldpath, newpath)
                    # _volume_converter(max_vol, oldpath, newpath_volmod)
                    # shutil.copy(newpath_volmod, newpath)
                    continue

                if oldpath != newpath:
                    shutil.copy(oldpath, newpath)

            else:
                continue

    # 処理の最後にフォルダの再スキャン
    cmd = [
        'docker-compose',
        'exec',
        '-u',
        'www-data',
        'app',
        './occ',
        'groupfolder:scan',
        json_load['GLOUPFOLDER_ID']
    ]
    subprocess.call(cmd, cwd='/home/ubuntu/nextcloud')


def command_stdout(args):
    json_open = open('./media_checker_env.json', 'r')
    json_load = json.load(json_open)

    input_dir = json_load['GROUPFOLDER_PATH'] + json_load['GLOUPFOLDER_ID']

    # 対象フォルダ配下の動画の情報をすべて標準出力する
    media_status = []

    duration_upper_limit = int("".join(args.upper_limit))
    duration_lower_limit = int("".join(args.lower_limit))

    list_of_dirs = glob.glob("".join(input_dir) + '/*')
    for list_of_each_dirs in list_of_dirs:
        list_of_files = glob.glob(list_of_each_dirs + '/*')
        for base_filename in list_of_files:
            try:
                media_width, media_height, media_duration, media_size = _get_media_info(base_filename)
            except (KeyError, UnboundLocalError):
                err_body = {
                        "status": "invalid_format",
                        "statistics": {
                            "ファイル名": base_filename,
                            "ファイルフォーマット": "ファイルの読み込みに失敗しました"
                            }
                        }
                media_status.append(err_body)
                continue

            filename = base_filename.split('/')[-1]

            # ファイルがMP4形式ではない場合
            if filename.split('.')[-1] != "mp4":
                check_datetime = str(datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime("%Y-%m-%d %H:%M:%S"))
                non_mp4 = {
                        "status": "invalid_format",
                        "statistics": {
                            "ファイル名": base_filename,
                            "最終チェック日時": check_datetime,
                            "ファイルフォーマット": "ファイルの読み込みに失敗しました(non mp4 format)"
                            }
                        }
                media_status.append(non_mp4)

            else:
                media_status_dict = _create_media_status(media_width,
                                                        media_height,
                                                        media_duration,
                                                        media_size,
                                                        duration_upper_limit,
                                                        duration_lower_limit,
                                                        filename)

                media_status_dict["statistics"]["ファイル名"] = base_filename

                media_status.append(media_status_dict)

    print(json.dumps(media_status, ensure_ascii=False))


def _get_media_info(filename):
    """
    対象の動画ファイルの情報を取得する

    Args:
        filename(str): 情報取得対象のファイル名(フルパス)
    Returns:
        media_width(int): 動画の横幅(px)
        media_height(int): 動画の縦幅(px)
        media_duration(int): 動画の長さ(sec)
        media_size(int): 動画のサイズ(byte)
    """

    # 指定したフォルダ配下の動画の情報を取得する
    get_proc_cmd = [
            'ffprobe',
            '-hide_banner',
            '-show_streams',
            '-show_format',
            '-of',
            'json',
            str(filename)
        ]

    proc_mediainfo = subprocess.run(
            get_proc_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    media_datas = json.loads(proc_mediainfo.stdout)

    for media_data in media_datas['streams']:
        if media_data['codec_type'] == "video" \
                and (media_data['codec_name'] == "h264" or media_data['codec_name'] == "hevc"):
            media_width = media_data['width']
            media_height = media_data['height']
            media_duration = int(media_data['duration'].split('.')[0])
    media_size = os.path.getsize(filename)

    return media_width, media_height, media_duration, media_size


def _create_media_status(
        media_width,
        media_height,
        media_duration,
        media_size,
        duration_upper_limit,
        duration_lower_limit,
        filename):
    """
    ファイルごとに動画情報を生成する

    Args:
        media_width(int): 動画の横幅(px)
        media_height(int): 動画の縦幅(px)
        media_duration(int): 動画の長さ(sec)
        media_size(int): 動画のサイズ(byte)
        duration_upper_limit(int): 動画の長さの上限
        duration_lower_limit(int): 動画の長さの下限
        filename(str): 動画ファイル名
    Returns:
        media_status_dict(dict): Dk上にAPI経由で送る動画情報
    """
    # 現在時刻の取得
    check_datetime = str(datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime("%Y-%m-%d %H:%M:%S"))

    # 解像度チェック
    if media_width < require_resolutions[lower_target_ratio]["width"] or \
            media_height < require_resolutions[lower_target_ratio]["height"]:
        resolution_status = "NG"
    elif require_resolutions[upper_target_ratio]["width"] < media_width or \
            require_resolutions[upper_target_ratio]["height"] < media_height:
        resolution_status = "NG"
    else:
        resolution_status = "OK"
    resolution_type = "NON STANDARD"

    # アスペクト比チェック
    if media_width % horizontal_criteria_ratio == 0 and \
            media_height % vertical_criteria_ratio == 0 and \
            media_width // horizontal_criteria_ratio == media_height // vertical_criteria_ratio:
        aspect_status = "OK"
        aspect_ratio = "16:9"
    else:
        aspect_status = "NG"
        aspect_ratio = "{} x {}".format(media_width, media_height)

    # 解像度が標準規格に沿っているかをチェックする
    for resolution_definition in require_resolutions:
        # check if standard
        if media_width == resolution_definition["width"] and \
                media_height == resolution_definition["height"]:
            set_ratio = resolution_definition["ratio"]
            if set_ratio == lower_target_ratio or \
                    set_ratio == upper_target_ratio:
                resolution_status = "OK"
            elif set_ratio != lower_target_ratio or \
                    set_ratio != upper_target_ratio:
                resolution_status = "NG"
            resolution_type = resolution_definition["type"]

            if media_width % 16 == 0 and media_height % 9 == 0:
                aspect_status = "OK"
                aspect_ratio = "16:9"
            else:
                aspect_status = "NG"
                aspect_ratio = "16:9ではありません: {} x {}".format(media_width, media_height)

    # 動画の長さのチェック
    media_duration_min = media_duration // 60
    if media_duration_min < duration_lower_limit:
        duration_status = "NG"
        duration_description = "基準値（{}分）を下回っています".format(duration_lower_limit)
    elif duration_lower_limit <= media_duration_min <= duration_upper_limit:
        duration_status = "OK"
        duration_description = "適切な動画の長さです"
    else:
        duration_status = "NG"
        duration_description = "基準値（{}分）を超えています".format(duration_upper_limit)

    # 動画のサイズチェック(if True)
    if size_flag:
        media_size_mib = media_size // (1024*1024)
        if media_size_mib >= size_upper_limit:
            size_status = "NG"
            size_description = "基準値（{}MB）を超えています".format(size_upper_limit)
        else:
            size_status = "OK"
            size_description = "基準値内の動画サイズです"
    else:
        size_status = False

    # BODY作成
    media_status_dict = {
        "status": "confirmed",
        "statistics": {
            "最終チェック日時": check_datetime,
            "解像度チェック": resolution_status,
            "解像度タイプ": resolution_type,
            "アスペクト比チェック": aspect_status,
            "アスペクト比": aspect_ratio,
            "動画の長さチェック": duration_status,
            "動画の長さコメント": duration_description
            }
        }

    if resolution_status != "OK" or \
            aspect_status != "OK" or \
            duration_status != "OK":
        media_status_dict["status"] = "invalid_format"

    if size_status:
        media_status_dict["statistics"]["ファイルサイズチェック"] = size_status
        media_status_dict["statistics"]["ファイルサイズコメント"] = size_description
        if size_status != "OK":
            media_status_dict["status"] = "invalid_format"

    return media_status_dict


def _send_errlog_to_slack(message, slack_url):
    """
    動画チェックの処理に失敗した際にSlack通知する

    Args:
        message(str): 発生したエラー詳細
        slack_url(str): Slack webhook url
    Returns:
    """
    header = {'content-type': 'application/json'}
    base_data = {
            "text": message
            }
    post_data = json.dumps(base_data, ensure_ascii=False).encode()

    slack_req = urllib.request.Request(slack_url,
                                       headers=header,
                                       data=post_data,
                                       method='POST')

    urllib.request.urlopen(slack_req)


def _dk_token_check(token):
    """
    dreamkast API tokenの有効期限を確認する

    Args:
        token(str): 現在保持しているtoken情報
    Returns:
        (bool): tokenの期限切れでない場合はTrue
    """
    token_payload = jwt.decode(token, options={"verify_signature": False})
    token_expire = datetime.datetime.fromtimestamp(token_payload['exp'])

    if datetime.datetime.now() < token_expire:
        return True
    else:
        return False


def _dk_token_update(domain, audience, client_id, client_secret):
    """
    dreamkast API tokenを更新する

    Args:
        domain(str): Dk API auth domain
        audience(str): Dk API auth audience
        client_id(str): Dk API auth client
        client_secret(str): Dk API auth secret
    Returns:
        None
    """
    url = 'https://' + domain + '/oauth/token'
    header = {
        "content-type": "application/json"
    }
    data = {
        "client_id": "",
        "client_secret": "",
        "audience": "",
        "grant_type": "client_credentials"
    }
    data['audience'] = audience
    data['client_id'] = client_id
    data['client_secret'] = client_secret

    req = urllib.request.Request(url,
                                 headers=header,
                                 data=json.dumps(data).encode(),
                                 method='POST'
                                 )

    res = urllib.request.urlopen(req)
    body = json.load(res)

    with open('./media_checker_env.json') as env:
        update_env = json.load(env, object_pairs_hook=OrderedDict)
        update_env['TOKEN'] = body['access_token']

    with open('./media_checker_env.json', 'w') as f:
        json.dump(update_env, f, indent=4, ensure_ascii=False)


def _check_volume(filename):
    """
    動画の音量を確認する

    Args:
        filename(str): 音量確認対象のファイル名
    Returns:
        output_max(str): 動画の最大音量
    """
    proc_maxVolume_cmd = [
            "ffmpeg",
            "-i",
            filename,
            "-vn",
            "-af",
            "volumedetect",
            "-f",
            "null",
            "-"
        ]
    proc_maxVolume = subprocess.Popen(
            proc_maxVolume_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    output = str(proc_maxVolume.stderr.read().decode())
    output_max = output.split("max_volume: ")[1].split(" dB")[0]

    return output_max


def _volume_converter(max_vol, input_file, output_file):
    """
    動画ファイルの音量を規格化する

    Args:
        max_vol(str): 動画の最大音量
        input_file(str): 変換元のファイル名
        output_file(str): 変換後のファイル名
    Returns:
        None
    """
    if "-" in max_vol:
        calc_val = max_vol.split("-")[1]
    else:
        calc_val = "-"+str(max_vol)

    proc_normalize_cmd = [
            "ffmpeg",
            "-i",
            input_file,
            "-vcodec",
            "copy",
            "-af",
            'volume={}dB'.format(calc_val),
            output_file
        ]
    subprocess.Popen(
            proc_normalize_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )


def get_args():
    parser = argparse.ArgumentParser(description="""
    動画の情報を取得し、判定条件を満たしているか否かを判定する
    """)

    subparsers = parser.add_subparsers()

    parser_put = subparsers.add_parser('put',
                                       help='セッションの最新ファイルごとに動画のチェック結果をDkにAPI経由で連携する')

    parser_put.add_argument('--csv',
                            nargs=1,
                            type=str,
                            required=True,
                            metavar='CSV_FILE',
                            help='セッションのCSVリスト')

    parser_put.add_argument('--upper_limit',
                            nargs=1,
                            type=str,
                            required=True,
                            metavar='DURATION_UPPER_LIMIT',
                            help='動画の長さの上限の指定(分)')

    parser_put.add_argument('--lower_limit',
                            nargs=1,
                            type=str,
                            required=True,
                            metavar='DURATION_LOWER_LIMIT',
                            help='動画の長さの下限の指定(分)')

    parser_put.set_defaults(handler=command_put)

    parser_stdout = subparsers.add_parser('stdout',
                                          help='指定のディレクトリ配下の全ての動画の情報を標準出力する')

    parser_stdout.add_argument('--upper_limit',
                               nargs=1,
                               type=str,
                               required=True,
                               metavar='DURATION_UPPER_LIMIT',
                               help='動画の長さの上限の指定(分)')

    parser_stdout.add_argument('--lower_limit',
                               nargs=1,
                               type=str,
                               required=True,
                               metavar='DURATION_LOWER_LIMIT',
                               help='動画の長さの下限の指定(分)')

    parser_stdout.set_defaults(handler=command_stdout)

    args = parser.parse_args()

    if hasattr(args, 'handler'):
        return args
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
