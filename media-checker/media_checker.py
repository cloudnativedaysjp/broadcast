#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import csv
from datetime import datetime
import glob
import json
import subprocess
import os
import sys
import urllib.request
import urllib.error

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
target_ratio = require_resolutions[2]["ratio"]
horizontal_criteria_ratio = 16
vertical_criteria_ratio = 9

# デフォルトのファイルサイズ(MB)判定基準
size_upper_limit = 2000
size_flag = True


def main():
    args = get_args()

    args.handler(args)


def command_put(args):
    # Dk連携用の環境変数がセットされているかを確認する
    # 環境変数($TOKEN/$DREAMKAST_DOMAIN)の確認
    if os.getenv('TOKEN') is None or \
            os.getenv('DREAMKAST_DOMAIN') is None:
        # 環境変数の存在が確認できない場合、その旨をSlack通知し処理を終了する
        message = "subject: $TOKEN" + '\r\n' +\
                  "環境変数の読み込みに失敗しました"
        _send_errlog_to_slack(message)
        sys.exit(1)

    # 動画が格納されているフォルダの第一階層のフォルダ名を取得する
    input_dir = args.input[0]
    # 末尾に / が存在する場合に削除
    input_dir = input_dir.rstrip('/')

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

    list_of_dirs = glob.glob("".join(args.input) + '/*')
    for row in list_csv_file:
        for dirs in list_of_dirs:
            dirs = dirs.split('/')[-1]
            if dirs.split('_')[0] == row[0]:
                list_of_files = glob.glob("".join(args.input) + '/' + row[0] + '*' + '/*')
                # フォルダ内の最新のファイルをフルパスで取得する
                try:
                    latest_file = max(list_of_files, key=os.path.getctime)
                except ValueError:
                    continue

                # 最新のファイルがMP4形式ではない場合
                if latest_file.split('.')[1] != "mp4":
                    filename = latest_file.split('/')[-1]
                    check_datetime = str(datetime.today().isoformat(timespec='seconds'))
                    non_mp4 = {
                            "status": "invalid_format",
                            "statistics": {
                                "ファイル名": filename,
                                "チェック日時": check_datetime,
                                "ファイルフォーマット": "ファイルの読み込みに失敗しました"
                                }
                            }
                    # Return to Dk
                    talkid = row[0]
                    url = 'https://' + os.getenv('DREAMKAST_DOMAIN') + '/api/v1/talks/' + talkid + '/video_registration'
                    header = {'Authorization': 'Bearer ' + os.getenv('TOKEN')}
                    put_data = json.dumps(non_mp4, ensure_ascii=False)

                    dk_nonmp4_req = urllib.request.Request(url,
                                                           headers=header,
                                                           data=put_data.encode(),
                                                           method='PUT')
                    try:
                        urllib.request.urlopen(dk_nonmp4_req)
                    except:
                        # Dk連携が失敗した場合にSlack通知
                        import traceback
                        message = "subject: " + filename + '\r\n' +\
                                  "reason: Dk連携に失敗しました" + '\r\n' +\
                                  "error detail: " + '\r\n' +\
                                  traceback.format_exc()
                        _send_errlog_to_slack(message)
                        sys.exit(1)

                    continue

                # 最新ファイルの動画情報を生成する
                try:
                    media_width, media_height, media_duration, media_size = _get_media_info(latest_file)
                except KeyError:
                    # 動画情報の取得に失敗した場合にSlack通知
                    import traceback
                    message = "subject: " + latest_file + '\r\n' +\
                              "reason: 動画情報の取得に失敗しました" + '\r\n' +\
                              "error detail: " + '\r\n' +\
                              traceback.format_exc()
                    _send_errlog_to_slack(message)
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
                url = 'https://' + os.getenv('DREAMKAST_DOMAIN') + '/api/v1/talks/' + talkid + '/video_registration'
                header = {'Authorization': 'Bearer ' + os.getenv('TOKEN')}
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
                    message = "subject: " + filename + '\r\n' +\
                              "reason: Dk連携に失敗しました" + '\r\n' +\
                              "error detail: " + '\r\n' +\
                              traceback.format_exc()
                    _send_errlog_to_slack(message)
                    sys.exit(1)

                # Dk連携が完了後、動画をRename
                oldpath = latest_file
                newpath = input_dir + "/" + dirs + "/" + row[1] + ".mp4"
                os.rename(oldpath, newpath)

            else:
                continue


def command_stdout(args):
    # 対象フォルダ配下の動画の情報をすべて標準出力する
    media_status = []

    duration_upper_limit = int("".join(args.upper_limit))
    duration_lower_limit = int("".join(args.lower_limit))

    list_of_dirs = glob.glob("".join(args.input) + '/*')
    for list_of_each_dirs in list_of_dirs:
        list_of_files = glob.glob(list_of_each_dirs + '/*')
        for filename in list_of_files:
            try:
                media_width, media_height, media_duration, media_size = _get_media_info(filename)
            except KeyError:
                err_body = {
                        "status": "invalid_format",
                        "statistics": {
                            "ファイル名": filename,
                            "ファイルフォーマット": "ファイルの読み込みに失敗しました"
                            }
                        }
                media_status.append(err_body)
                continue
            filename = filename.split('/')[-1]
            media_status_dict = _create_media_status(media_width,
                                                     media_height,
                                                     media_duration,
                                                     media_size,
                                                     duration_upper_limit,
                                                     duration_lower_limit,
                                                     filename)

            media_status.append(media_status_dict)

    print(json.dumps(media_status, ensure_ascii=False))


def _get_media_info(filename):
    """
    対象の動画ファイルの情報を取得する

    Args:
        filename(str): 情報取得対象のファイル名
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
    media_data = json.loads(proc_mediainfo.stdout)

    media_width = media_data['streams'][0]['width']
    media_height = media_data['streams'][0]['height']
    media_duration = int(media_data['format']['duration'].split('.')[0])
    media_size = int(media_data['format']['size'])

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
    check_datetime = str(datetime.today().isoformat(timespec='seconds'))

    # 解像度チェック
    if media_width < require_resolutions[target_ratio]["width"] or \
            media_height < require_resolutions[target_ratio]["height"]:
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
            size_description = "基準値（{}GB）を超えています".format(size_upper_limit)
        else:
            size_status = "OK"
            size_description = "基準値内の動画サイズです"
    else:
        size_status = False

    # BODY作成
    media_status_dict = {
        "status": "confirmed",
        "statistics": {
            "ファイル名": filename,
            "チェック日時": check_datetime,
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


def _send_errlog_to_slack(message):
    """
    動画チェックの処理に失敗した際にSlack通知する

    Args:
        message(str): 発生したエラー詳細
    Returns:
    """
    slack_url = os.getenv('SLACKURL')
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


def get_args():
    parser = argparse.ArgumentParser(description="""
    動画の情報を取得し、判定条件を満たしているか否かを判定する
    """)

    subparsers = parser.add_subparsers()

    parser_put = subparsers.add_parser('put',
                                       help='セッションの最新ファイルごとに動画のチェック結果をDkにAPI経由で連携する')

    parser_put.add_argument('--input',
                            nargs=1,
                            type=str,
                            required=True,
                            metavar='INPUT',
                            help='セッション動画格納先ディレクトリ')

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
                                          help='指定のディレクトリは以下の動画情報を全て標準出力する')

    parser_stdout.add_argument('--input',
                               nargs=1,
                               type=str,
                               required=True,
                               metavar='INPUT',
                               help='セッション動画格納先ディレクトリ')

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
