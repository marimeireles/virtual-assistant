from rasa_sdk import Action
from rasa_sdk.events import SlotSet

# class ActionInternetSearch(Action):

class ActionNotSure(Action):
   def name(self):
      return "action_not_sure"

   def run(self, dispatcher, tracker, domain):
    print("🌸")
    print(tracker, '🦋')
    result = "brabuletinha"
    return [SlotSet("search", ["brabuletinha"])]