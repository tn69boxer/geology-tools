import csv
import sys
import platform
from datetime import datetime

LOG_FILE = "field_samples.csv"

def get_gps():
    os_name = platform.system()
    if os_name == "Linux" or os_name == "Darwin":
        return get_gps_gpsd()
    elif os_name == "Android":
        return get_gps_termux()
    else:
        return get_gps_ip()

def get_gps_termux():
    try:
        import subprocess
        import json
        result = subprocess.run(
            ["termux-location", "-p", "gps", "-r", "once"],
            capture_output=True, text=True, timeout=30
        )
        data = json.loads(result.stdout)
        return data["latitude"], data["longitude"], "termux"
    except Exception:
        return get_gps_ip()

def get_gps_gpsd():
    try:
        import gps
        session = gps.gps(mode=gps.WATCH_ENABLE)
        report = session.next()
        while report['class'] != 'TPV':
            report = session.next()
        return report.lat, report.lon, "gpsd"
    except Exception:
        return get_gps_ip()

def get_gps_ip():
    try:
        import urllib.request
        import json
        url = "https://ipinfo.io/json"
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read())
        lat, lon = data["loc"].split(",")
        return float(lat), float(lon), "ip"
    except Exception:
        return get_gps_manual()

def get_gps_manual():
    print("Could not get GPS automatically.")
    lat = float(input("Enter latitude: "))
    lon = float(input("Enter longitude: "))
    return lat, lon, "manual"

def add_entry(sample_name, notes, lat=None, lon=None, source=None):
    if lat is None:
        lat, lon, source = get_gps()
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, time, sample_name, lat, lon, notes, source])
    print(f"Logged: {sample_name} at {lat}, {lon} ({source})")

def view_logs():
    try:
        with open(LOG_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                print(f"{row[0]} {row[1]} | {row[2]} | {row[3]}, {row[4]} | {row[6]} | {row[5]}")
    except FileNotFoundError:
        print("No samples logged yet.")

def summary():
    totals = {}
    try:
        with open(LOG_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                source = row[6]
                totals[source] = totals.get(source, 0) + 1
        total_samples = sum(totals.values())
        print(f"--- Summary ---")
        print(f"Total samples: {total_samples}")
        for source, count in totals.items():
            print(f"  {source}: {count} samples")
    except FileNotFoundError:
        print("No samples logged yet.")

if len(sys.argv) < 2:
    print("Usage: python3 fieldlog.py <command> [args]")
    print("Commands: add <sample_name> <notes> [lat] [lon]")
    print("          view")
    print("          summary")
    sys.exit(1)

if sys.argv[1] == "add":
    if len(sys.argv) == 6:
        add_entry(sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5]), "manual")
    elif len(sys.argv) == 4:
        add_entry(sys.argv[2], sys.argv[3])
    else:
        print("Usage: add <sample_name> <notes> [lat lon]")
elif sys.argv[1] == "view":
    view_logs()
elif sys.argv[1] == "summary":
    summary()
else:
    print("Unknown command. Use: add, view, summary")

def view_logs():
    try:
        with open(LOG_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                print(f"{row[0]} {row[1]} | {row[2]} | {row[3]}, {row[4]} | {row[6]} | {row[5]}")
    except FileNotFoundError:
        print("No samples logged yet.")

def summary():
    totals = {}
    try:
        with open(LOG_FILE, "r") as f:
            reader = csv.reaader(f)
            for row in reader:
                source = row[6]
                totals[source] = totals.get(source, 0) + 1
        total_samples =sum(totals.values())
        print(f"--- Summary ---")
        print(f"Total samples: {total_samples}")
        for source, count in totals.items():
            print(f"  {source}: {count} samples")
    except FileNotFoundError:
        print("No samples logged yet.")
