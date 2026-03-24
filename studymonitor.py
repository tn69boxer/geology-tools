import argparse
import csv
import json
import os
import sys
from datetime import datetime, date

LOG_FILE = "study_log.csv"
ACTIVE_SESSIONS_FILE = "active_sessions.json"

def load_active_sessions():
    if os.path.exists(ACTIVE_SESSIONS_FILE):
        with open(ACTIVE_SESSIONS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_active_sessions(sessions):
    with open(ACTIVE_SESSIONS_FILE, 'w') as f:
        json.dump(sessions, f, default=str)

def add_entry(topic, duration, notes):
    today = str(date.today())
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([today, topic, duration, notes])
    print(f"Logged: {topic} - {duration} mins on {today}")

def start_session(topic, subtopic):
    sessions = load_active_sessions()
    if topic in sessions:
        print(f"Session for {topic} is already active.")
        return
    sessions[topic] = {
        'start_time': datetime.now().isoformat(),
        'subtopic': subtopic
    }
    save_active_sessions(sessions)
    print(f"Started session for {topic}: {subtopic}")

def end_session(topic):
    sessions = load_active_sessions()
    if topic not in sessions:
        print(f"No active session for {topic}.")
        return
    start_time_str = sessions[topic]['start_time']
    start_time = datetime.fromisoformat(start_time_str)
    duration = int((datetime.now() - start_time).total_seconds() / 60)
    subtopic = sessions[topic]['subtopic']
    notes = f"{subtopic} session"
    add_entry(topic, duration, notes)
    del sessions[topic]
    save_active_sessions(sessions)
    print(f"Ended session for {topic}: {duration} mins")

def view_logs():
    try:
        with open(LOG_FILE, "r") as f:
            reader = csv.reader(f)
            print("Date | Topic | Duration (mins) | Notes")
            print("-" * 50)
            for row in reader:
                print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
    except FileNotFoundError:
        print("No logs yet.")

def summary():
    totals = {}
    sessions_count = {}
    try:
        with open(LOG_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                topic = row[1]
                duration = int(row[2])
                totals[topic] = totals.get(topic, 0) + duration
                sessions_count[topic] = sessions_count.get(topic, 0) + 1
        print("--- Summary ---")
        for topic in totals:
            print(f"{topic}: {sessions_count[topic]} sessions, {totals[topic]} mins")
        print(f"Total: {sum(totals.values())} mins")
    except FileNotFoundError:
        print("No logs yet.")

def main():
    parser = argparse.ArgumentParser(description="Study Monitor CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    start_parser = subparsers.add_parser('start', help='Start a study session')
    start_parser.add_argument('topic', help='Topic name')
    start_parser.add_argument('subtopic', help='Subtopic name')

    end_parser = subparsers.add_parser('end', help='End a study session')
    end_parser.add_argument('topic', help='Topic name')

    subparsers.add_parser('view', help='View all logs')
    subparsers.add_parser('summary', help='View summary of logs')

    args = parser.parse_args()

    if args.command == 'start':
        start_session(args.topic, args.subtopic)
    elif args.command == 'end':
        end_session(args.topic)
    elif args.command == 'view':
        view_logs()
    elif args.command == 'summary':
        summary()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
