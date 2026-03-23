import csv
import sys
from datetime import date

LOG_FILE = "study_log.csv"

def add_entry(topic, notes):
    today = str(date.today())
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([today, topic, notes])
    print(f"Logged: {topic} on {today}")

add_entry(sys.argv[1], sys.argv[2])
