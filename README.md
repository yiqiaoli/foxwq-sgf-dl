# go-sgf-analyzer

`go-sgf-analyzer` is a Python utility designed to download and analyze Go game records in SGF format from the FoxWQ
platform. This tool provides a convenient way to programmatically access and process Go game records for analysis and
study.

## Features

- Download SGF files directly from FoxWQ.
- Scan and recognize the images of a board and generate SGF files.
- Easy to use command-line interface.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes.

### Prerequisites

Before you begin, ensure you have Python installed on your system. You can download Python
from [here](https://www.python.org/downloads/). This project uses Python 3.7 or later.

### Installation

To install `go-sgf-analyzer`, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/go-sgf-analyzer.git
    cd foxwq-sgf-dl
    ```

2. **Set up a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the package**:
    ```bash
    pip install .
    ```

4. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

To use `go-sgf-analyzer`, you can execute the command-line interface or import the package in your Python scripts:

**Command-line example**:

```bash
# Example command to download and analyze games
python foxwq_sgf_dl --download [options]
```
