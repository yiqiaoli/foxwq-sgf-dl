# foxwq-sgf-dl

A Python package for downloading Go game records from FoxWQ.

## Features

- Download all or a specific number of game records for a given user.
- Filter games by user ID or username.
- Save downloaded go game records in SGF format.
- Keep track of downloaded games to avoid duplicate downloads.
- Flexible configuration options

## Requirements

- Python 3.6+
- Required packages (install with `pip install -r requirements.txt`)

## Installation

To use this package, you first need to have Python installed. Follow these steps to set it up:

1. **Clone the Repository**:

   ```shell
   git clone https://github.com/yiqiaoli/foxwq-sgf-dl.git
   ```
2. **Navigate to the Project Directory**:
   ```shell
   cd foxwq-sgf-dl
   ```
3. **Install Dependencies: If you're using `venv`**:

   ```shell
   python -m venv venv
   source venv/bin/activate
   ```
   Install the requirements:
   ```shell
   pip install -r requirements.txt
   ```
   Alternatively, you can install the package directly:
   ```shell
   pip install . 
   ```

## Usage

### Command-Line Help

To view the help information for the command-line tool, use:

```shell
foxwq_sgf_dl --help
```

### How to run the package

After setting up the package, you can run the following commands:

#### **Download All Games**:
```shell
foxwq_sgf_dl --config path/to/config.cfg --all-games
```

Replace `path/to/config.cfg` with the path to your configuration file.

#### **Download Recent Games**:
```shell
foxwq_sgf_dl --config path/to/config.cfg --number-of-games 10
```

Replace `10` with the desired number of recent games to download.

#### **Download Games with `foxwq_sgf_dl` (Default Behavior)**:
```shell
foxwq_sgf_dl
```

When run without any options, `foxwq_sgf_dl` uses the default configuration file and downloads all games unless a
specific number of recent games is specified in the configuration file.

### For Developers

Alternatively, run the package directly using the command:

```shell
python -m foxwq_sgf_dl.downloader
```

## Configuration

Before running the tool, you need to configure the `config.cfg` file. Below is an example configuration:

```ini
[DEFAULT]
# User identifier and password used for login
login_identifier = <your_login_identifier>
password = <your_password>

# Authentication details
# - Source user ID (uid) to fetch game records
# - Timestamp for the API requests
# - Authentication token
# - Session ID
srcuid = <your_source_uid>
time_stamp = <your_timestamp>
token = <your_token>
session = <your_session>

# Username to search for specific games
search_username = <your_search_username>

# Directory to save downloaded game records (SGF files)
directory = ../games

```

**Note**: The login API can be used to obtain `srcuid`, `time_stamp`, and `token`,
but we haven't yet figured out how session is calculated from those three.
Currently, these values are hardcoded in the configuration file.

### Sample Configuration File

A sample configuration file is provided as `sample_config.cfg` for your reference.
Rename the `sample_config.cfg` to `config.cfg` if you use it as a template.  



## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.



## Acknowledgments
Special thanks to 李炯介(Ivan Li) and the FoxWQ community.
