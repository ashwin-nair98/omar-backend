import json
import operator
from pprint import pprint
from watson_developer_cloud import AssistantV1, LanguageTranslatorV3
import os

class WatsonAPI():

    def __init__(self):
        self.assistant = AssistantV1(
            username = os.getenv('WATSON_ASSISTANT_USER'),
            password = os.getenv('WATSON_ASSISTANT_PASSWORD'),
            version='2017-04-21')
        self.assistant.set_http_config({'timeout': 100})

    def get_response(self, dialog, context):
        """
        Calls Watson API and returns the response.
        """
        response = self.assistant.message(
            workspace_id=os.getenv('WATSON_WORKSPACE_ID'),
            input={
                'text': dialog
            },
            context=context)
        return response


class WatsonArabicAPI():
    def __init__(self):
        self.assistant = AssistantV1(
            username = os.getenv('WATSON_ASSISTANT_USER'),
            password = os.getenv('WATSON_ASSISTANT_PASSWORD'),
            version='2017-04-21')
        self.assistant.set_http_config({'timeout': 100})
        self.translator = LanguageTranslatorV3(version='2018-05-01',
            username='a387cdeb-cf27-4e9b-ba38-2ebf3ae082f0', 
            password='JNxORYhqXi4a')

    
    def get_response(self, dialog, context):
        """
        Calls Watson API and returns the response.
        """
        response = self.assistant.message(
            workspace_id=os.getenv('WATSON_WORKSPACE_ARABIC_ID'),
            input={
                'text': dialog
            },
            context=context)
        pprint(response)
        return response
    
    def translate_to_arabic(self, string):
        print("From: ", string)
        res =  self.translator.translate(string, source='en', target='ar')['translations'][0]['translation']
        print("To: ", res)
        return res