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
from rasa_sdk.forms import FormAction

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


class ContactForm(FormAction):
    def name(self) -> Text:
        return "contact_form"

    def required_slots(tracker):
        return ["person", "email"]        


class ActionSubmitContactForm(Action):

    def name(self) -> Text:
        return "action_submit_contact_form"

    def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slot_name = tracker.get_slot("person")
        email = tracker.get_slot("email")
        name = extract_name(slot_name, nlp)
        data = {"name": name, "email": email}
        add_contact(data)
        confirmation_message = "Dodano kontakt {} o emailu {}".format(name, email)
        dispatcher.utter_message(confirmation_message)
        return [SlotSet("person", name)]


class ActionGetForex(Action):

    def name(self) -> Text:
        return "action_get_forex"

    def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        rates = get_currency_rates()
        dispatcher.utter_message(text=rates)
        return []

