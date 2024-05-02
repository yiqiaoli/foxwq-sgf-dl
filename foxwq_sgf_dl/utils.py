from sgfmill import sgf
import logging


def get_headers():
    """Reusable headers for requests."""
    return {
        'User-Agent': "UnityPlayer/2022.1.16f1 (UnityWebRequest/1.0, libcurl/7.84.0-DEV)",
        'Accept-Encoding': "deflate, gzip",
        'Content-Type': "application/json",
        'referer': "http://www.qq.com",
        'X-Unity-Version': "2022.1.16f1"
    }


def correct_komi(sgf_data_375):
    """Correct the Komi in the SGF data for sgf_data from Foxwq"""
    return sgf_data_375.replace("\\r\\n", "\n").replace('KM[375]', 'KM[7.5]')


def save_sgf_file(sgf_data, full_path):
    """Save SGF data to a file."""
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
