"""
Web‑based diagnostic dashboard.

Creates a Flask application with endpoints for system statistics and driver information.
"""

from flask import Flask, jsonify
import psutil
import wmi

app = Flask(__name__)


@app.route('/')
def index():
    return 'Diagnostic Dashboard'


@app.route('/stats')
def stats():
    data = {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent,
    }
    return jsonify(data)


@app.route('/drivers')
def drivers():
    c = wmi.WMI()
    drivers_list = []
    for d in c.Win32_PnPSignedDriver():
        drivers_list.append({'device': d.DeviceName, 'version': d.DriverVersion})
    return jsonify(drivers_list)


if __name__ == '__main__':
    app.run()