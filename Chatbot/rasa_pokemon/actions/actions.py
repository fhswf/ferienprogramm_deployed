from typing import Any, Text, Dict, List
from pathlib import Path

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, Restarted

import requests

class ActionCheckExistence(Action):
    knowledge = Path("data/pokenames.txt").read_text().split("\n")

    def name(self) -> Text:
        return "action_check_existence"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        for blob in tracker.latest_message['entities']:
            print(tracker.latest_message)
            if blob['entity'] == 'pokemon_name':
                name = blob['value']
                if name in self.knowledge:
                    dispatcher.utter_message(text=f"Ja, {name} ist ein Pokemon.")
                else:
                    dispatcher.utter_message(text=f"Ich kenne {name} nicht.")
        return []
   

