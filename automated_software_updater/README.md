# Automated Software Updater

This script identifies installed packages and updates them to approved versions. On Windows the script calls winget or chocolatey. On Linux the script calls apt. The script logs each update.

## Features

- Detects the operating system and package manager.
- Reads desired versions from a JSON file.
- Compares installed versions with desired versions.
- Runs update commands and logs actions.

## Prerequisites

- Python 3.8 or later.
- Administrative privileges for installing updates.
- Install dependencies from `requirements.txt`.

## Setup

1. Install dependencies (none beyond the standard library).
2. Prepare `desired_versions.json` with package names and target versions.
3. Run the script:
   ```
   python main.py
   ```