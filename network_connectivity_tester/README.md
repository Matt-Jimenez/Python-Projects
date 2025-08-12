# Network Connectivity Tester

This script tests reachability and latency for a list of hosts. The script reads IP addresses or hostnames from a text file, pings each host, measures latency and packet loss, and records the results.

## Features

- Reads hostnames or IPs from `hosts.txt`.
- Pings each host and measures round‑trip time.
- Records success rate and average latency.
- Writes results to `results.csv`.

## Prerequisites

- Python 3.8 or later.
- Install dependencies from `requirements.txt`.

## Setup

1. Install dependencies (none beyond the standard library).
2. Populate `hosts.txt` with one host per line.
3. Run the script:
   ```
   python main.py
   ```