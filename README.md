# foxwq-sgf-dl

A Python package for downloading Go game records from FoxWQ.

## Features

- Login and authenticate with FoxWQ
- Download Go game records (SGF format)
- Retrieve user information
- Flexible configuration options

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
3. **Install Dependencies:If you're using `venv`**:
   ```shell
   python -m venv venv
   source venv/bin/activate  # on Linux/MacOS
   venv\Scripts\activate.bat  # on Windows
   ```
   Then install the requirements:
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

### For Non-Developers
After setting up the package, you can run the following commands:
1. **Download All Games**:
   ```shell
   foxwq_sgf_dl --config path/to/config.cfg --all-games
   ```
Replace `path/to/config.cfg` with the path to your configuration file.

2. **Download Recent Games**:
   ```shell
   foxwq_sgf_dl --config path/to/config.cfg --number-of-games 10
   ```
Replace `10` with the desired number of recent games to download.

3. **Download Games with `foxwq_sgf_dl` (Default Behavior):
   ```shell
   foxwq_sgf_dl
   ```
When run without any options, `foxwq_sgf_dl` uses the default configuration file and downloads all games unless a specific number of recent games is specified in the configuration file.

### For Developers
Developers can run the package directly using the command:
```shell
python -m foxwq_sgf_dl.downloader
```

## Configuration
The package reads configuration from a `.cfg` file. An example configuration file might look like this:
```ini
[DEFAULT]
user_identifier = "your_username"
password = "your_password"
srcuid = 1233456
username = "target_username"
time_stamp = 1714582201198
token = "your_token"
session = "your_session"
directory = "../games"
```

### Sample Configuration File
A sample configuration file is provided as `sample_config.cfg` for your reference.




















