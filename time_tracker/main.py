from gcal_client import GoogleCalendarClient
from categorizer import EventCategorizer
from notion_tracker import NotionTimeTracker
import os
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    print("Connecting to Google Calendar...")
    gcal = GoogleCalendarClient()
    
    print("Connecting to Notion...")
    notion_token = os.getenv('NOTION_TOKEN')
    notion = NotionTimeTracker(notion_token)
    
    print("Initializing OpenAI categorizer...")
    categorizer = EventCategorizer()

    print("\nFetching events from calendar...")
    events = gcal.get_events(days_back=1)
    print(f"Found {len(events)} events")
    for event in events:
        print(f"Event: {event['summary']}, Start: {event['start']['dateTime']}, End: {event['end']['dateTime']}")

    print("\nCategorizing events...")
    categorized_events = categorizer.batch_categorize(events)

    print("\nSaving to Notion...")
    for event in categorized_events:
        print(event['summary'])
        notion.create_event_entry(event)
        print(f"Saved: {event['summary']} - {event['category']}")

    print("\nDone! Check your Notion database.")

if __name__ == "__main__":
    main() 