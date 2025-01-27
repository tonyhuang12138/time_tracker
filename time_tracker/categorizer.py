from openai import OpenAI
import os
from typing import List, Dict

class EventCategorizer:
    def __init__(self):
        # Get key from environment variable
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        if not self.client.api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        self.categories = [
            "Productive Moment",
            "Brainrot",
            "Exercise", 
            "Social",
            "Other"
        ]

    def categorize_event(self, event_title: str) -> str:
        """Categorize a single event using OpenAI's API"""
        prompt = f"""You are a text-categorization bot.
Classify this activity into one of these categories: {', '.join(self.categories)}.
The activity is: "{event_title}".
Please respond with the single best category.

Guidelines:
- "Productive Moment" for work, study, or any focused productive activity
- "Brainrot" for entertainment, idle browsing, or non-productive leisure
- "Exercise" for physical activities and workouts
- "Social" for interactions with friends and family
- "Other" for anything that doesn't fit above

In your response, only return the category name, no other text.
"""


        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a precise categorization assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=50
        )

        return response.choices[0].message.content.strip()

    def batch_categorize(self, events: List[Dict]) -> List[Dict]:
        """Categorize a batch of events"""
        for event in events:
            event['category'] = self.categorize_event(event['summary'])
        return events