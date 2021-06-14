# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker,FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import  SlotSet, EventType
from rasa_sdk.types import DomainDict

from rasa_sdk import Action
from .SalesforceDatabase_Connectivity import sf_api_call
import requests
import json
import re

class ActionResourcesList(Action):

    def name(self) -> Text:
        return "action_resources_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        covid_resources = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [{
                    "title": "Sales Cloud",
                    "subtitle": "Experience :- 3-5 Yrs, Location :- Banglore",
                    "image_url": "https://www.crmwave.com/uploads/6/1/1/8/61183005/8870397_orig.png",
                    "buttons": [{
                            "title": "Apply Now",
                            "type": "postback",
                            "payload": "/apply_now"
                        }
                    ]
                },
                    {
                        "title": "Service Cloud",
                        "subtitle": "Experience :- 3-5 Yrs, Location :- Banglore",
                        "image_url": "https://cloud-elements.com/wp-content/uploads/2018/12/salesforce-service-cloud-logo-600.jpg",
                        "buttons": [{
                                "title": "Apply Now",
                                "type": "postback",
                                "payload": "/apply_now"
                            }
                        ]
                    },
                    {
                        "title": "Community Cloud",
                        "subtitle": "Experience :- 3-5 Yrs, Location :- Banglore",
                        "image_url": "https://cloud4good.com/wp-content/uploads/2016/08/salesforce-community-cloud2.jpg",
                        "buttons": [{
                                "title": "Apply Now",
                                "type": "postback",
                                "payload": "/apply_now"
                            }
                        ]
                    },
                    {
                        "title": "RASA CHATBOT",
                        "subtitle": "Conversational AI",
                        "image_url": "static/rasa.png",
                        "buttons": [{
                            "title": "Rasa",
                            "url": "https://www.rasa.com",
                            "type": "web_url"
                        },
                            {
                                "title": "Rasa Chatbot",
                                "type": "postback",
                                "payload": "/greet"
                            }
                        ]
                    }
                ]
            }
        }

        dispatcher.utter_message(attachment=covid_resources)
        return []


class ValidateRestaurantForm(Action):
    def name(self) -> Text:
        return "user_details_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["name", "number", "mailid"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]

class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "Dict",
    ) -> List[Dict[Text, Any]]:

     sf_api_call('/services/data/v40.0/sobjects/Rasa__c/', method="post", data={
         'First_Name__c': tracker.get_slot("name"),
          'Mobile_No__c':tracker.get_slot("number"),
         'Email__c': tracker.get_slot("mailid")
         })
     dispatcher.utter_message(response="utter_details_thanks",
                                 Name=tracker.get_slot("name"),
                                 Mobile_number=tracker.get_slot("number"),
                                 Email=tracker.get_slot("mailid"))

     return [SlotSet('name',None),SlotSet('number',None),SlotSet('mailid',None)]    

class ValidateRestaurantForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_user_details_form"

     

    def validate_mailid(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        value1 = tracker.get_slot('mailid')
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

        if(re.search(regex, value1)):
         print("Valid Email") 
         return {"mailid": slot_value}
        else:
         print("Invalid Email")
         dispatcher.utter_message(text="your mail address is not in the email format, Please enter your mail address in valid email format ")
         return {"mailid": None}


    def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:


        if len(slot_value) <= 2:
         print("InValid Name")
         dispatcher.utter_message(text="the name is very short") 
         return {"name": None} 
         
        else:
         print("Valid Name")
         return {"name": slot_value}

    def validate_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        value1 = tracker.get_slot('number')
        pattern = r"[789]\d{9}$"

        if re.match(pattern,value1):
         print("Valid number") 
         return {"number": slot_value}
        else:
         print("Invalid Number")
         dispatcher.utter_message(text="Please enter your 10 digits Mobile Number ")
         return {"number": None}  
