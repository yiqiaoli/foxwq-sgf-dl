import requests
import json
import hashlib
import configparser
from sgfmill import sgf
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_headers():
    """Reusable headers for requests."""
    return {
        'User-Agent': "UnityPlayer/2022.1.16f1 (UnityWebRequest/1.0, libcurl/7.84.0-DEV)",
        'Accept-Encoding': "deflate, gzip",
        'Content-Type': "application/json",
        'referer': "http://www.qq.com",
        'X-Unity-Version': "2022.1.16f1"
    }


def api_request(method, url, params=None, data=None):
    """Send an API request and return the response JSON, or None on failure."""
    try:
        if method.lower() == 'get':
            response = requests.get(url, params=params, headers=get_headers())
        elif method.lower() == 'post':
            response = requests.post(url, data=data, headers=get_headers())
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"{method.upper()} request failed: {e}")
        return None


def login(username, password):
    url = "https://newframe.foxwq.com/cgi/LoginByPassword"
    hash_object = hashlib.md5(password.encode('utf-8'))
    md5_hash = hash_object.hexdigest()  # Get the hexadecimal representation of the digest
    payload = json.dumps({
        "device_id_md5": "e7ab56438d7225217c9a417a87031fef",
        "client_type": 13,
        "password": md5_hash,
        "user_identifier": username
    })
    return api_request('post', url, data=payload)


def query_user_info_by_uid(srcuid, dstuid, time_stamp):
    url = "https://newframe.foxwq.com/cgi/QueryUserInfoPanel"
    params = {
        'srcuid': srcuid,
        'dstuid': dstuid,
        'time_stamp': time_stamp
    }
    return api_request('get', url, params=params)


def query_user_info_by_username(srcuid, username, time_stamp):
    url = "https://newframe.foxwq.com/cgi/QueryUserInfoPanel"
    params = {
        'srcuid': srcuid,
        'username': username,
        'time_stamp': time_stamp
    }
    return api_request('get', url, params=params)


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
    response = api_request('get', url, params=params)
    return response['chesslist'] if response else []


def get_kifu_by_id(chess_id, srcuid, time_stamp, token, session):
    url = "https://newframe.foxwq.com/chessbook/TXWQFetchChess"
    params = {
        'chessid': chess_id,
        'trans': chess_id,
        'srcuid': srcuid,
        'time': time_stamp,
        'token': token,
        'session': session
    }
    response = api_request('get', url, params=params)
    if response:
        sgf_data_375 = response['chess']
        return correct_komi(sgf_data_375)
    return None


def correct_komi(sgf_data_375):
    """Correct the Komi in the SGF data for sgf_data from Foxwq"""
    return sgf_data_375.replace("\\r\\n", "\n").replace('KM[375]', 'KM[7.5]')


def save_sgf_file(sgf_data, full_path):
    try:
        with open(full_path, 'w') as f:
            f.write(sgf_data.strip())
    except IOError as e:
        logging.error(f"Failed to save SGF file {full_path}: {e}")


def generate_filename_from_sgf(sgf_data):
    """Generate a filename from SGF data properties."""
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
        logging.error(f"Error processing SGF data: {e}")
        return "error_game.sgf"


def download_all_kifu(srcuid, dstuid, time_stamp, token, session, directory):
    games = get_all_games(srcuid, dstuid, time_stamp, token, session)
    for game in games:
        sgf_data = get_kifu_by_id(game['chessid'], srcuid, time_stamp, token, session)
        if sgf_data:
            file_name = generate_filename_from_sgf(sgf_data) + game['chessid'] + '.sgf'
            if not os.path.exists(directory):
                os.makedirs(directory)
            full_path = os.path.join(directory, file_name)
            save_sgf_file(sgf_data, full_path)


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
