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


def view_logs():
    try:
        with open(LOG_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                print(f"{row[0]} | {row[1]} | {row[2]} mins | {row[3]}")
    except FileNotFoundError:
     print("No logs yet.")

def summary():
    totals = {}
    sessions = {}
    try:
        with open(LOG_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                topic = row[1]
                duration = int(row[2])
                totals[topic] = totals.get(topic, 0) + duration
                sessions[topic] = sessions.get(topic, 0) + 1
        print("--- Summary ---")
        for topic in totals:
            print(f"{topic}: {sessions[topic]} sessions, {totals[topic]} mins")
        print(f"Total: {sum(totals.values())} mins")
    except FileNotFoundError:
        print("No logs yet.")



if sys.argv[1] == "add":
    add_entry(sys.argv[2], sys.argv[3], sys.argv[4])
elif sys.argv[1] == "view":
    view_logs()
elif sys.argv[1] == "summary":
    summary()
else:
    print("Unknown command. Use: add <topic> <duration> <notes> OR view")
