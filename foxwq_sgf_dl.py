import requests
import json
import base64
import configparser


def login():
    url = "https://newframe.foxwq.com/cgi/LoginByPassword"
    payload = json.dumps({
        "device_id_md5": "e7ab56438d7225217c9a417a87031fef",
        "client_type": 13,
        "password": "bd857aa217fe4f11989dc86f15957284",
        "user_identifier": "ciaobella"
    })
    headers = {
        'User-Agent': "UnityPlayer/2022.1.16f1 (UnityWebRequest/1.0, libcurl/7.84.0-DEV)",
        'Accept-Encoding': "deflate, gzip",
        'Content-Type': "application/json",
        'referer': "http://www.qq.com",
        'X-Unity-Version': "2022.1.16f1"
    }
    response = requests.post(url, data=payload, headers=headers)
    return response.json()


def query_user_info_by_uid(srcuid, dstuid, time_stamp):
    url = "https://newframe.foxwq.com/cgi/QueryUserInfoPanel"
    params = {
        'srcuid': srcuid,
        'dstuid': dstuid,
        'time_stamp': time_stamp
    }
    headers = {
        'User-Agent': "UnityPlayer/2022.1.16f1 (UnityWebRequest/1.0, libcurl/7.84.0-DEV)",
        'Accept-Encoding': "deflate, gzip",
        'X-Unity-Version': "20  22.1.16f1"
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()


def query_user_info_by_username(srcuid, username, time_stamp):
    url = "https://newframe.foxwq.com/cgi/QueryUserInfoPanel"
    params = {
        'srcuid': srcuid,
        'username': username,
        'time_stamp': time_stamp
    }
    headers = {
        'User-Agent': "UnityPlayer/2022.1.16f1 (UnityWebRequest/1.0, libcurl/7.84.0-DEV)",
        'Accept-Encoding': "deflate, gzip",
        'X-Unity-Version': "20  22.1.16f1"
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()


def get_kifu_list(srcuid, dstuid, time_stamp, token, session):
    url = "https://newframe.foxwq.com/chessbook/TXWQFetchChessList"

    params = {
        'type': "1",
        'fetchnum': "70",
        'dstuid': dstuid,
        'srcuid': srcuid,
        'time': time_stamp,
        'token': token,
        'session': session
    }

    headers = {
        'User-Agent': "UnityPlayer/2022.1.16f1 (UnityWebRequest/1.0, libcurl/7.84.0-DEV)",
        'Accept-Encoding': "deflate, gzip",
        'X-Unity-Version': "2022.1.16f1"
    }
    response = requests.get(url, params=params, headers=headers)
    # last_chessid = response.json()['chesslist'][0]['chessid']
    # return last_chessid
    return response.json()


def get_kifu_by_id(chess_id, srcuid, time_stamp, token, session):
    url = "https://newframe.foxwq.com/chessbook/TXWQFetchChess"
    headers = {
        'User-Agent': "UnityPlayer/2022.1.16f1 (UnityWebRequest/1.0, libcurl/7.84.0-DEV)",
        'Accept-Encoding': "deflate, gzip",
        'X-Unity-Version': "2022.1.16f1"
    }
    params = {
        'chessid': chess_id,
        'trans': chess_id,
        'srcuid': srcuid,
        'time': time_stamp,
        'token': token,
        'session': session
    }
    response = requests.get(url, params=params, headers=headers)
    old_text_to_replace = 'KM[375]'
    new_text_to_replace = 'KM[7.5]'
    return response.json()['chess'].replace("\\r\\n", "\n").replace(old_text_to_replace, new_text_to_replace)


def save_sgf_file(sgf_data, sgf_file_path):
    with open(sgf_file_path, 'w') as f:
        f.write(sgf_data.strip())


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('foxwq.cfg')
    token = config['DEFAULT']['token']
    srcuid = config['DEFAULT']['srcuid']
    username = config['DEFAULT']['username']
    time_stamp = config['DEFAULT']['time_stamp']
    token = config['DEFAULT']['token']
    session = config['DEFAULT']['session']
    sgf_file_path = config['DEFAULT']['sgf_file_path']
