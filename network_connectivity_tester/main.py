"""
Network connectivity tester.

Reads hosts from hosts.txt, pings each host, and writes success and latency results to results.csv.
"""

import subprocess
import csv

HOSTS_FILE = 'hosts.txt'
OUTPUT_FILE = 'results.csv'


def ping_host(host):
    """Ping a host and return a tuple: (success, average latency in ms or None)."""
    try:
        result = subprocess.run([
            'ping',
            '-c',
            '4',
            host
        ], capture_output=True, text=True)
        success = result.returncode == 0
        latency = None
        if success:
            for line in result.stdout.splitlines():
                if 'avg' in line:
                    parts = line.split('=')
                    if len(parts) > 1:
                        avg = parts[1].split('/')[1]
                        latency = float(avg)
        return success, latency
    except Exception:
        return False, None


def test_connectivity():
    """Read hosts and test connectivity."""
    with open(HOSTS_FILE) as f:
        hosts = [line.strip() for line in f if line.strip()]
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Host', 'Success', 'AverageLatency'])
        for host in hosts:
            success, latency = ping_host(host)
            writer.writerow([host, success, latency or 'N/A'])


if __name__ == '__main__':
    test_connectivity()