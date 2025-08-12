# Web‑Based Diagnostic Dashboard

This project provides a simple web interface for running diagnostics. The script uses Flask to create web routes for system information, driver status, and network tests.

## Features

- Defines a Flask application with routes for diagnostics【693104849707234†L45-L79】.
- Displays CPU, memory, disk, and network statistics.
- Lists driver status and version comparison.
- Allows users to start network tests from the browser.

## Prerequisites

- Python 3.8 or later.
- Install dependencies from `requirements.txt`.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the web application:
   ```
   flask --app main run
   ```
3. Open your browser at `http://127.0.0.1:5000/` to use the dashboard.