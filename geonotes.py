import csv
import sys
from datetime import date

LOG_FILE = "study_log.csv"

def add_entry(topic, duration, notes):
    today = str(date.today())
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([today, topic, duration, notes])
    print(f"Logged: {topic} - {duration} mins on {today}")

add_entry(sys.argv[1], sys.argv[2], sys.argv[3])
