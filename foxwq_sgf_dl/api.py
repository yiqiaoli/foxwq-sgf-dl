import requests
import json
import hashlib
import logging
from .utils import get_headers, correct_komi


def api_request(method, url, params=None, data=None):
    """Send an API request and return the response JSON, or None on failure."""
    try:
        response = requests.request(method, url, headers=get_headers(),
                                    json=data if method.lower() == 'post' else None,
                                    params=params if method.lower() == 'get' else None)
        response.raise_for_status()
        logging.info(f"Success {method.upper()} request to {url}")
        return response.json()
    except requests.HTTPError as e:
        logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        return None
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None


def login(user_identifier, password):
    """Authenticate user and return session details."""
    url = "https://newframe.foxwq.com/cgi/LoginByPassword"
    hash_object = hashlib.md5(password.encode('utf-8'))
    md5_hash = hash_object.hexdigest()  # Get the hexadecimal representation of the digest
    # json.dumps() seems redundant, but it gives error without it
    payload = json.dumps({
        "device_id_md5": "e7ab56438d7225217c9a417a87031fef",
        "client_type": 13,
        "password": md5_hash,
        "user_identifier": user_identifier
    })
    return api_request('post', url, data=payload)


def query_user_info_by_uid(srcuid, dstuid, time_stamp):
    """Fetch user information by UID."""
    url = "https://newframe.foxwq.com/cgi/QueryUserInfoPanel"
    params = {
        'srcuid': srcuid,
        'dstuid': dstuid,
        'time_stamp': time_stamp
    }
    return api_request('get', url, params=params)


def query_user_info_by_username(srcuid, username, time_stamp):
    """Fetch user information by username."""
    url = "https://newframe.foxwq.com/cgi/QueryUserInfoPanel"
    params = {
        'srcuid': srcuid,
        'username': username,
        'time_stamp': time_stamp
    }
    return api_request('get', url, params=params)


def get_game_metadata_list(srcuid, dstuid, time_stamp, token, session, last_id=None, number_of_games=None):
    """Retrieve a list of game metadata."""
    url = "https://newframe.foxwq.com/chessbook/TXWQFetchChessList"
    params = {
        'type': 1,
        'fetchnum': str(number_of_games) if number_of_games else "",
        'dstuid': dstuid,
        'srcuid': srcuid,
        'time': time_stamp,
        'token': token,
        'session': session,
        'lastCode': last_id
    }
    response = api_request('get', url, params=params)
    if response and 'chesslist' in response:
        return response['chesslist']
    else:
        logging.warning("Response from API is missing 'chesslist' key or is empty.")
        return []


def get_game_details(chess_id, srcuid, time_stamp, token, session):
    """Fetch detailed game record by game ID."""
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
    if response and 'chess' in response:
        sgf_data_375 = response['chess']
        return correct_komi(sgf_data_375)
    else:
        logging.warning(f"Response from API is missing 'chess' key for chess ID {chess_id}.")
        return None
