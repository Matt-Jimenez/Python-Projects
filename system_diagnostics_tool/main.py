"""
System diagnostics tool.

Collects and prints system statistics using the psutil library.
"""

import json
from datetime import datetime
import psutil


def collect_stats():
    """Gather system statistics and return them as a dictionary."""
    stats = {
        'timestamp': datetime.now().isoformat(),
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent,
        'net_bytes_sent': psutil.net_io_counters().bytes_sent,
        'net_bytes_recv': psutil.net_io_counters().bytes_recv,
    }
    return stats


def main():
    stats = collect_stats()
    print(json.dumps(stats, indent=2))


if __name__ == '__main__':
    main()