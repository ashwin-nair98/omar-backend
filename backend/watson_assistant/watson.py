import json
import operator
from pprint import pprint
from watson_developer_cloud import AssistantV1

class WatsonAPI():

    def __init__(self):
        with open('config.json') as f:
            self.config = json.load(f)
            self.assistant = AssistantV1(
                username = self.config['username'],
                password= self.config['password'],
                version='2017-04-21')
            self.assistant.set_http_config({'timeout': 100})
    
    
    
    
    def get_response(self, dialog, context):
        """
        Calls Watson API and returns the response.
        """
        response = self.assistant.message(
            workspace_id=self.config['workspace_id'], 
            input={
                'text': dialog
            }, 
            context=context)
        return response