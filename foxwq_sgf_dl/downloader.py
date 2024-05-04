import os
import logging
import configparser
import argparse
import json
from .api import get_kifu_list, get_kifu_by_id, query_user_info_by_username
from .utils import save_sgf_file, generate_filename_from_sgf


def setup_logging(log_path=None):
    """Setup logging for the application."""
    if log_path is None:
        log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'debug.log')
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler(log_path), logging.StreamHandler()])


def parse_arguments():
    parser = argparse.ArgumentParser(description="Download game records.")
    parser.add_argument('-c', '--config', help='Path to the configuration file.', default=None)
    parser.add_argument('-u', '--username', help='Specify a username to download their game records.', default=None)

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-n', '--number-of-games', type=int,
                       help='Specify the number of recent games to download. '
                            'If omitted, defaults to downloading all games unless --all-games is specified.',
                       default=None)
    group.add_argument('--all-games', action='store_true',
                       help='Download all games. Overrides --number-of-games if both are specified.')
    return parser.parse_args()


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


def get_uid_by_username(username, srcuid, time_stamp):
    """Fetch UID by username."""
    user_info = query_user_info_by_username(srcuid, username, time_stamp)
    if user_info and 'uid' in user_info:
        return user_info['uid']
    else:
        logging.error(f"Failed to retrieve UID for username: {username}")
        return None


def download_all_kifu(srcuid, dstuid, time_stamp, token, session, base_directory):
    """Download all available Kifu records to a specified directory."""
    player_directory = os.path.join(base_directory, dstuid)
    if not os.path.exists(player_directory):
        os.makedirs(player_directory, exist_ok=True)
    downloaded_ids = load_downloaded_game_ids(player_directory)

    try:
        games = get_all_games(srcuid, dstuid, time_stamp, token, session)
        for game in games:
            if game['chessid'] in downloaded_ids:
                continue
            sgf_data = get_kifu_by_id(game['chessid'], srcuid, time_stamp, token, session)
            if sgf_data:
                file_name = generate_filename_from_sgf(sgf_data) + game['chessid'] + '.sgf'
                full_path = os.path.join(player_directory, file_name)
                save_sgf_file(sgf_data, full_path)
                downloaded_ids.add(game['chessid'])
        save_downloaded_game_ids(downloaded_ids, player_directory)
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


def download_recent_games(srcuid, dstuid, time_stamp, token, session, base_directory, number_of_games):
    """Download a specific number of recent game records. The number of recent games should be less than 100."""
    player_directory = os.path.join(base_directory, dstuid)
    if not os.path.exists(player_directory):
        os.makedirs(player_directory, exist_ok=True)
    downloaded_ids = load_downloaded_game_ids(player_directory)
    games = get_kifu_list(srcuid, dstuid, time_stamp, token, session, number_of_games=number_of_games)
    if games:
        for game in games:
            if game['chessid'] in downloaded_ids:
                continue  # Skip already downloaded games
            sgf_data = get_kifu_by_id(game['chessid'], srcuid, time_stamp, token, session)
            if sgf_data:
                file_name = generate_filename_from_sgf(sgf_data) + game['chessid'] + '.sgf'
                full_path = os.path.join(player_directory, file_name)
                save_sgf_file(sgf_data, full_path)
                downloaded_ids.add(game['chessid'])
        save_downloaded_game_ids(downloaded_ids, player_directory)
        logging.info(f"Downloaded the last {number_of_games} games.")
    else:
        logging.info("No games available to download.")


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


def load_downloaded_game_ids(player_directory):
    """ Load the set of downloaded game IDs from a file in the player's directory. """
    filepath = os.path.join(player_directory, 'downloaded_game_ids.json')
    try:
        with open(filepath, 'r') as file:
            return set(json.load(file))
    except FileNotFoundError:
        return set()


def save_downloaded_game_ids(downloaded_ids, player_directory):
    """ Save the set of downloaded game IDs to a file in the player's directory. """
    filepath = os.path.join(player_directory, 'downloaded_game_ids.json')
    with open(filepath, 'w') as file:
        json.dump(list(downloaded_ids), file)


def main():
    args = parse_arguments()
    setup_logging(args.log_path)
    try:
        config = load_config(args.config)
        user_identifier = config.get('DEFAULT', 'user_identifier')
        password = config.get('DEFAULT', 'password')
        srcuid = config.get('DEFAULT', 'srcuid')
        username = config.get('DEFAULT', 'username')
        time_stamp = config.get('DEFAULT', 'time_stamp')
        token = config.get('DEFAULT', 'token')
        session = config.get('DEFAULT', 'session')
        directory = config.get('DEFAULT', 'directory', fallback='../games')

        dstuid = srcuid  # Default to srcuid
        if args.username is not None:
            dstuid = get_uid_by_username(args.username, srcuid, time_stamp)
        elif username:
            dstuid = get_uid_by_username(username, srcuid, time_stamp)
        if not dstuid:
            logging.error("UID could not be retrieved for the provided username. Aborting operation.")
            return
        if args.number_of_games is not None:
            download_recent_games(srcuid, dstuid, time_stamp, token, session, directory, args.number_of_games)
        elif args.all_games:
            download_all_kifu(srcuid, dstuid, time_stamp, token, session, directory)
        else:
            # Default action if no specific command is provided
            download_all_kifu(srcuid, dstuid, time_stamp, token, session, directory)

    except Exception as e:
        logging.error(f"An error occurred during execution: {e}")


if __name__ == '__main__':
    main()
