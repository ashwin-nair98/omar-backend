import json
import operator
from pprint import pprint
from watson_developer_cloud import AssistantV1
import os

class WatsonAPI():

    def __init__(self):
        self.assistant = AssistantV1(
            username = os.getenv('WATSON_USER'),
            password = os.getenv('WATSON_PASSWORD'),
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
