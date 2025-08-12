# Hardware and Driver Checker

This project inspects hardware devices and drivers on Windows machines using the WMI interface. The script lists devices, driver versions, and start modes and compares them against approved versions.

## Features

- Queries Win32 classes such as `Win32_SystemDriver` and `Win32_PnPSignedDriver`.
- Lists installed devices and driver versions.
- Compares versions with an approved list from JSON.
- Produces a report recommending updates.

## Prerequisites

- Python 3.8 or later.
- Windows with WMI available.
- Install dependencies from `requirements.txt`.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Prepare `approved_versions.json` with device names and version numbers.
3. Run the script:
   ```
   python main.py
   ```