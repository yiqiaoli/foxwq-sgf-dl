import os
import logging
import configparser
import argparse
import json
from .api import login, get_game_metadata_list, get_game_details, query_user_info_by_username
from .utils import save_sgf_file, generate_filename_from_sgf


def setup_logging(log_path=None):
    """Setup logging for the application."""
    if log_path is None:
        log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'debug.log')
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler(log_path), logging.StreamHandler()])


def parse_arguments():
    parser = argparse.ArgumentParser(description="Download Go game records from FoxWQ.")
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
        config_path = os.path.join(base_dir, 'sample_config.cfg')
        print(f"No custom config provided. Using default config at {config_path}")

    config = configparser.ConfigParser()
    if not config.read(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    validate_config(config)
    return config


def get_uid_by_username(username, srcuid, time_stamp):
    """Fetch UID by username."""
    user_info = query_user_info_by_username(srcuid, username, time_stamp)
    if user_info and 'uid' in user_info:
        return user_info['uid']
    else:
        logging.error(f"Failed to retrieve UID for username: {username}")
        return None


def download_all_games(srcuid, dstuid, time_stamp, token, session, base_directory):
    """Download all available game records to a specified directory."""
    player_directory = os.path.join(base_directory, dstuid)
    if not os.path.exists(player_directory):
        os.makedirs(player_directory, exist_ok=True)
    downloaded_ids = load_downloaded_game_ids(player_directory)
    games = []  # Used to remember actual games downloaded this time

    try:
        game_metadata_list = get_all_game_metadata(srcuid, dstuid, time_stamp, token, session)
        for metadata in game_metadata_list:
            if metadata['chessid'] in downloaded_ids:
                continue
            sgf_data = get_game_details(metadata['chessid'], srcuid, time_stamp, token, session)
            if sgf_data:
                file_name = generate_filename_from_sgf(sgf_data) + metadata['chessid'] + '.sgf'
                full_path = os.path.join(player_directory, file_name)
                save_sgf_file(sgf_data, full_path)
                downloaded_ids.add(metadata['chessid'])
                games.append(metadata)
        save_downloaded_game_ids(downloaded_ids, player_directory)
        logging.info(f"Successfully downloaded {len(games)} games.")
    except Exception as e:
        logging.error(f"Error downloading Kifu records: {e}")


def get_all_game_metadata(srcuid, dstuid, time_stamp, token, session):  # get all kifu
    """Fetch all games iteratively."""
    all_metadata = []
    last_id = None
    while True:
        metadata_list = get_game_metadata_list(srcuid, dstuid, time_stamp, token, session, last_id)
        if not metadata_list:
            break  # Break the loop if no more games are returned
        all_metadata.extend(metadata_list)
        last_id = metadata_list[-1]['chessid']  # Update last_id to the last game's ID in the batch
    return all_metadata


def download_recent_games(srcuid, dstuid, time_stamp, token, session, base_directory, number_of_games):
    """Download a specific number of recent game records. The number of recent games should be less than 100."""
    player_directory = os.path.join(base_directory, dstuid)
    if not os.path.exists(player_directory):
        os.makedirs(player_directory, exist_ok=True)
    downloaded_ids = load_downloaded_game_ids(player_directory)
    games = []
    game_metadata_list = get_game_metadata_list(srcuid, dstuid, time_stamp, token, session,
                                                number_of_games=number_of_games)
    if game_metadata_list:
        for metadata in game_metadata_list:
            if metadata['chessid'] in downloaded_ids:
                continue  # Skip already downloaded games
            sgf_data = get_game_details(metadata['chessid'], srcuid, time_stamp, token, session)
            if sgf_data:
                file_name = generate_filename_from_sgf(sgf_data) + metadata['chessid'] + '.sgf'
                full_path = os.path.join(player_directory, file_name)
                save_sgf_file(sgf_data, full_path)
                downloaded_ids.add(metadata['chessid'])
                games.append(metadata)
        save_downloaded_game_ids(downloaded_ids, player_directory)
        logging.info(f"Downloaded the last {number_of_games} games.")
    else:
        logging.info("No games available to download.")


def validate_config(config):
    """Validate required configuration keys."""
    required_keys = ['user_identifier', 'password', 'srcuid', 'time_stamp', 'token', 'session', 'directory']
    missing_keys = [key for key in required_keys if not config.get('DEFAULT', key, fallback=None)]
    if missing_keys:
        raise ValueError(f"Missing required configuration keys: {', '.join(missing_keys)}")


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
    setup_logging()
    try:
        config = load_config(args.config)
        login_identifier = config.get('DEFAULT', 'login_identifier')
        password = config.get('DEFAULT', 'password')
        srcuid = config.get('DEFAULT', 'srcuid')
        search_username = config.get('DEFAULT', 'search_username')
        time_stamp = config.get('DEFAULT', 'time_stamp')
        token = config.get('DEFAULT', 'token')
        session = config.get('DEFAULT', 'session')
        directory = config.get('DEFAULT', 'directory', fallback='../games')

        # # Get srcuid from login
        # login_response = login(login_identifier, password)
        # if not login_response or 'uid' not in login_response:
        #     logging.error("Login failed or 'uid' not found in response. Aborting operation.")
        #     return
        # srcuid = login_response['uid']

        dstuid = srcuid  # Default to srcuid
        if args.username is not None:
            dstuid = get_uid_by_username(args.username, srcuid, time_stamp)
        elif search_username:
            dstuid = get_uid_by_username(search_username, srcuid, time_stamp)
        if not dstuid:
            logging.error("UID could not be retrieved for the provided search_username. Aborting operation.")
            return
        if args.number_of_games is not None:
            download_recent_games(srcuid, dstuid, time_stamp, token, session, directory, args.number_of_games)
        elif args.all_games:
            download_all_games(srcuid, dstuid, time_stamp, token, session, directory)
        else:
            # Default action if no specific command is provided
            download_all_games(srcuid, dstuid, time_stamp, token, session, directory)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Execution interrupted.")
    except Exception as e:
        logging.error(f"An error occurred during execution: {e}")
    else:
        logging.info("Execution completed successfully.")


if __name__ == '__main__':
    main()
