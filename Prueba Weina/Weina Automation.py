import time
from getpass import getpass
from datetime import datetime, timedelta

users = {}
events = {}

def create_account():
    username = input("Enter a username: ")
    if username in users:
        print("Username already exists.")
        return
    password = getpass("Enter a password: ")
    users[username] = password
    print("Account created successfully.")

def login():
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")
    if username in users and users[username] == password:
        print(f"Welcome, {username}!")
        return username
    else:
        print("Invalid credentials.")
        return None

def create_event(user):
    event_id = len(events) + 1
    title = input("Enter event title: ")
    description = input("Enter event description: ")
    start_time = input("Enter start time (YYYY-MM-DD HH:MM): ")
    duration = int(input("Enter duration in minutes: "))
    reminder_time = int(input("Enter reminder time before event (in minutes): "))

    start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    events[event_id] = {
        "title": title,
        "description": description,
        "start_time": start_datetime,
        "duration": duration,
        "reminder_time": reminder_time,
        "owner": user,
        "shared_with": {}
    }
    print(f"Event '{title}' created successfully!")

def list_events(user):
    print(f"Events for {user}:")
    for event_id, event in events.items():
        if event["owner"] == user or user in event["shared_with"]:
            print(f"{event_id}: {event['title']} - {event['description']} at {event['start_time']}")

def share_event(user):
    event_id = int(input("Enter the event ID to share: "))
    if event_id in events and events[event_id]["owner"] == user:
        share_with = input("Enter the username to share the event with: ")
        permission = input("Enter permission level (view/edit): ").lower()
        if share_with in users:
            events[event_id]["shared_with"][share_with] = permission
            print(f"Event shared with {share_with} with {permission} permissions.")
        else:
            print("User not found.")
    else:
        print("You do not own this event or it doesn't exist.")

def check_reminders():
    current_time = datetime.now()
    for event_id, event in events.items():
        event_time = event["start_time"]
        reminder_time = event_time - timedelta(minutes=event["reminder_time"])
        if reminder_time <= current_time <= event_time:
            print(f"Reminder: Event '{event['title']}' starts soon!")

def main():
    print("Welcome to the Event Scheduler and Reminder System")
    while True:
        print("\n1. Create account\n2. Login\n3. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            create_account()
        elif choice == '2':
            user = login()
            if user:
                while True:
                    print("\n1. Create event\n2. List events\n3. Share event\n4. Check reminders\n5. Logout")
                    user_choice = input("Choose an option: ")
                    if user_choice == '1':
                        create_event(user)
                    elif user_choice == '2':
                        list_events(user)
                    elif user_choice == '3':
                        share_event(user)
                    elif user_choice == '4':
                        check_reminders()
                    elif user_choice == '5':
                        print("Logged out.")
                        break
        elif choice == '3':
            print("Goodbye!")
            break
main()
