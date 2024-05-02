import requests
import json
import hashlib
import configparser
from sgfmill import sgf
import os


def login(username, password):
    url = "https://newframe.foxwq.com/cgi/LoginByPassword"
    hash_object = hashlib.md5()
    hash_object.update(password.encode('utf-8'))
    md5_hash = hash_object.hexdigest()  # Get the hexadecimal representation of the digest
    payload = json.dumps({
        "device_id_md5": "e7ab56438d7225217c9a417a87031fef",
        "client_type": 13,
        "password": md5_hash,
        "user_identifier": username
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


def get_kifu_list(srcuid, dstuid, time_stamp, token, session, last_id=None):
    url = "https://newframe.foxwq.com/chessbook/TXWQFetchChessList"
    params = {
        'type': "1",
        'fetchnum': "",
        'dstuid': dstuid,
        'srcuid': srcuid,
        'time': time_stamp,
        'token': token,
        'session': session,
        'lastCode': last_id
    }
    headers = {
        'User-Agent': "UnityPlayer/2022.1.16f1 (UnityWebRequest/1.0, libcurl/7.84.0-DEV)",
        'Accept-Encoding': "deflate, gzip",
        'X-Unity-Version': "2022.1.16f1"
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()['chesslist']
    else:
        return []


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
    sgf_data_375 = response.json()['chess']
    sgf_data = correct_komi(sgf_data_375)
    return sgf_data


def get_all_games(srcuid, dstuid, time_stamp, token, session):  # get all kifu
    all_games = []
    last_id = None
    while True:
        games = get_kifu_list(srcuid, dstuid, time_stamp, token, session, last_id)
        if not games:
            break  # Break the loop if no more games are returned
        all_games.extend(games)
        last_id = games[-1]['chessid']  # Update last_id to the last game's ID in the batch
    return all_games


def correct_komi(sgf_data_375):
    old_text_to_replace = 'KM[375]'
    new_text_to_replace = 'KM[7.5]'
    return sgf_data_375.replace("\\r\\n", "\n").replace(old_text_to_replace, new_text_to_replace)


def save_sgf_file(sgf_data, full_path):
    with open(full_path, 'w') as f:
        f.write(sgf_data.strip())


def create_filename_from_sgf(sgf_data):
    try:
        sgf_game = sgf.Sgf_game.from_string(sgf_data)

        root_node = sgf_game.get_root()
        date = root_node.get("DT")
        black_name = root_node.get("PB")
        white_name = root_node.get("PW")

        black_name = black_name if black_name is not None else "Unknown_Black"
        white_name = white_name if white_name is not None else "Unknown_White"

        filename = f"[{date}][{black_name}]vs[{white_name}]"
        return filename
    except Exception as e:
        print(f"Error processing SGF: {e}")
        return None


def download_all_kifu(srcuid, dstuid, time_stamp, token, session, directory):
    # games = get_kifu_list(srcuid, dstuid, time_stamp, token, session)
    games = get_all_games(srcuid, dstuid, time_stamp, token, session)
    for game in games:
        sgf_data = get_kifu_by_id(game['chessid'], srcuid, time_stamp, token, session)
        file_name = create_filename_from_sgf(sgf_data) + game['chessid'] + '.sgf'
        if not os.path.exists(directory):
            os.makedirs(directory)
        full_path = os.path.join('./games/', file_name)
        save_sgf_file(sgf_data, full_path)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('foxwq.cfg')
    srcuid = config['DEFAULT']['srcuid']
    username = config['DEFAULT']['username']
    password = config['DEFAULT']['password']
    time_stamp = config['DEFAULT']['time_stamp']
    token = config['DEFAULT']['token']
    session = config['DEFAULT']['session']
    directory = config['DEFAULT']['directory']
    download_all_kifu(srcuid, srcuid, time_stamp, token, session, directory)
