from notion_client import Client
from datetime import datetime
from typing import Dict, List
import os

class NotionTimeTracker:
    def __init__(self, token: str):
        self.notion = Client(auth=token)
        # Use the database ID from environment
        self.database_id = os.getenv('NOTION_DATABASE_ID')
        if not self.database_id:
            raise ValueError("NOTION_DATABASE_ID not found in environment variables")

    def create_event_entry(self, event: Dict) -> None:
        """Create a new entry in Notion database for an event"""
        properties = {
            "Title": {"title": [{"text": {"content": event['summary']}}]},
            "Start Time": {"date": {"start": event['start']['dateTime']}},
            "End Time": {"date": {"start": event['end']['dateTime']}},
            "Category": {"select": {"name": event['category']}},
            "Duration (mins)": {"number": self._calculate_duration(
                event['start']['dateTime'], 
                event['end']['dateTime']
            )}
        }

        self.notion.pages.create(
            parent={"database_id": self.database_id},
            properties=properties
        )
    
    def _calculate_duration(self, start: str, end: str) -> int:
        """Calculate duration in minutes between start and end times"""
        start_time = datetime.fromisoformat(start.replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(end.replace('Z', '+00:00'))
        return int((end_time - start_time).total_seconds() / 60) 