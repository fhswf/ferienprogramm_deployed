from http import client
from typing import Any, Text, Dict, List
from pathlib import Path

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, Restarted
from babel.dates import format_date, format_datetime, format_time

import requests
import python_weather
import asyncio

from .reqtest import getFromWiki


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
   

class ActionCheckWeather(Action):
    async def getweather(self, dispatcher: CollectingDispatcher):
        client = python_weather.Client(format=python_weather.METRIC)
        weather = await client.find("Iserlohn")
        dispatcher.utter_message(text=f"Die Temparatur ist {weather.current.temperature} Grad Celsius.")
        for forecast in weather.forecasts:
            dispatcher.utter_message(format_date(forecast.date, locale='de_DE'), "Die Temperatur wird: " + str(forecast.temperature) + " Grad Celsius.")
        await client.close()

    def name(self) -> Text:
        return "action_check_weather"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        await self.getweather(dispatcher)
            
        return []

class ActionGetAbilities(Action):
    knowledge = Path("data/pokenames.txt").read_text().split("\n")

    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("Hallo")

        for blob in tracker.latest_message['entities']:
            print(tracker.latest_message)
            if blob['entity'] == 'pokemon_name':
                name = blob['value']
                if name in self.knowledge:
                    getFromWiki().getPokemon(name, dispatcher)
                else:
                    dispatcher.utter_message(text=f"Ich kenne {name} nicht.")
        return []
    
    def name(self) -> Text:
        return "action_get_pokemon"
