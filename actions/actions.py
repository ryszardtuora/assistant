# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import spacy
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from contact_utils import extract_name, add_contact
from api_utils import get_currency_rates

nlp = spacy.load("pl_spacy_model_morfeusz")
test_doc = nlp("to jest dokument testowy")

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")
        return []


class ActionAddContact(Action):

    def name(self) -> Text:
        return "action_add_contact" # definiujemy nazwę akcji dla RASY

    def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = tracker.latest_message["text"] # pobranie wiadomości od użytkownika
        extracted_name = extract_name(message, nlp) # ekstrakcja znormalizowanego nazwiska i imienia
        if extracted_name: # ekstrakcja się udała -> zapisujemy dane w pliku
            add_contact(extracted_name)
            confirmation_message = "Dodano kontakt: {}.".format(extracted_name)
            dispatcher.utter_message(text=confirmation_message)
        else: # ekstrakcja się nie udała, prosimy o ponowienie
            error_message  = "Nie zrozumiałem imienia lub nazwiska tej osoby, proszę powtórz polecenie."
            dispatcher.utter_message(text=error_message)
        return [SlotSet("person", extracted_name)]


class ActionGetForex(Action):

    def name(self) -> Text:
        return "action_get_forex"

    def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        rates = get_currency_rates()
        dispatcher.utter_message(text=rates)
        return []



