import os
import logging
import configparser
import argparse
from .api import login, get_kifu_list, get_kifu_by_id, query_user_info_by_username
from .utils import save_sgf_file, generate_filename_from_sgf


def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler("debug.log"),
                            logging.StreamHandler()
                        ])


def parse_arguments():
    parser = argparse.ArgumentParser(description="Download game records.")
    parser.add_argument('-c', '--config', help='Path to the configuration file.', default=None)
    parser.add_argument('-u', '--username', help='Specify a username to download their game records.', default=None)
    return parser.parse_args()


def get_uid_by_username(username, srcuid, time_stamp):
    """Fetch UID by username."""
    user_info = query_user_info_by_username(srcuid, username, time_stamp)
    if user_info and 'uid' in user_info:
        return user_info['uid']
    else:
        logging.error(f"Failed to retrieve UID for username: {username}")
        return None


def download_all_kifu(srcuid, dstuid, time_stamp, token, session, directory):
    """Download all available Kifu records to a specified directory."""
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    try:
        games = get_all_games(srcuid, dstuid, time_stamp, token, session)
        for game in games:
            sgf_data = get_kifu_by_id(game['chessid'], srcuid, time_stamp, token, session)
            if sgf_data:
                file_name = generate_filename_from_sgf(sgf_data) + game['chessid'] + '.sgf'
                full_path = os.path.join(directory, file_name)
                save_sgf_file(sgf_data, full_path)
    except Exception as e:
        logging.error(f"Error downloading Kifu records: {e}")


def get_all_games(srcuid, dstuid, time_stamp, token, session):  # get all kifu
    """Fetch all games iteratively."""
    all_games = []
    last_id = None
    while True:
        games = get_kifu_list(srcuid, dstuid, time_stamp, token, session, last_id)
        if not games:
            break  # Break the loop if no more games are returned
        all_games.extend(games)
        last_id = games[-1]['chessid']  # Update last_id to the last game's ID in the batch
    return all_games


# def validate_config(config):
#     """Validate required configuration keys."""
#     required_keys = ['srcuid', 'username', 'password', 'time_stamp', 'token', 'session', 'directory']
#     for key in required_keys:
#         if key not in config['DEFAULT']:
#             raise ValueError(f"Missing required configuration key: {key}")
#
#
# def sanitize_filename(filename):
#     """Remove or replace characters in filenames that are invalid for file systems."""
#     invalid_chars = '<>:"/\\|?*'
#     for char in invalid_chars:
#         filename = filename.replace(char, '_')
#     return filename


def load_config(config_path=None):
    """Load configuration from a given path or use the default configuration."""
    if config_path is None:
        # Load default configuration from the package directory
        base_dir = os.path.dirname(os.path.dirname(__file__))
        config_path = os.path.join(base_dir, 'config.cfg')
        print(f"No custom config provided. Using default config at {config_path}")

    config = configparser.ConfigParser()
    if not config.read(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    # validate_config(config)
    return config


def main():
    setup_logging()
    args = parse_arguments()

    try:
        config = load_config(args.config)
        user_identifier = config['DEFAULT']['user_identifier']
        password = config['DEFAULT']['password']
        srcuid = config['DEFAULT']['srcuid']
        username = config['DEFAULT']['username']
        time_stamp = config['DEFAULT']['time_stamp']
        token = config['DEFAULT']['token']
        session = config['DEFAULT']['session']
        directory = config['DEFAULT']['directory']

        dstuid = srcuid  # Default to srcuid
        if args.username is not None:
            dstuid = get_uid_by_username(args.username, srcuid, time_stamp)
        elif username:
            dstuid = get_uid_by_username(username, srcuid, time_stamp)
        if not dstuid:
            logging.error("UID could not be retrieved for the provided username. Aborting operation.")
            dstuid = srcuid
        download_all_kifu(srcuid, dstuid, time_stamp, token, session, directory)
    except Exception as e:
        logging.error(f"An error occurred during execution: {e}")


if __name__ == '__main__':
    main()
