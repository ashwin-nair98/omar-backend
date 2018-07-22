from .watson import WatsonAPI
from .google import GoogleAPI
from pprint import pprint

class Conversation():
    def __init__(self):
        self.wapi = WatsonAPI()
        self.gapi = GoogleAPI()
        pass

    def locate_restaurant(self, params, context, result):
        restaurant_data = self.gapi.find_restaurant(context, params['cuisine'])
        context[result] = restaurant_data
        return context

    def find_route(self, params, context, result):
        response = self.gapi.find_route(context)
        context[result] = response
        return context

    def open_maps(self, params, context, result):
        response = self.gapi.find_url(context)
        context[result] = response
        return context

    def exit_chat(self, params, context, result):
        context[result] = True
        return context

    def message(self, message, context):
        wapi_response = self.wapi.get_response(message, context)
        if('actions' in wapi_response):
            action = wapi_response['actions'][0]['name']
            params = wapi_response['actions'][0]['parameters']
            result_variable = wapi_response['actions'][0]['result_variable']
            switcher_action = {
                'locate_restaurant': self.locate_restaurant,
                'find_route': self.find_route,
                'open_maps': self.open_maps,
                'exit_chat': self.exit_chat
            }
            switcher_result = {
                'context.restaurant': 'restaurant',
                'context.route': 'route',
                'context.map': 'map',
                'context.exit': 'exit'
            }
            action_function = switcher_action[action]
            result_variable = switcher_result[result_variable]
            watson_context = action_function(params, wapi_response['context'], result_variable)
            if 'exit' in watson_context:
                return {
                    'text': wapi_response['output']['text'][0],
                    'context': watson_context
                }
            wapi_response = self.wapi.get_response(None, watson_context)
        if('output' in wapi_response and 'context' in wapi_response):
            # pprint(wapi_response)
            text = wapi_response['output']['text'][0]
            context = wapi_response['context']
            return {
                'text': text,
                'context': context
            }
        else:
            return {
                'text': 'Something went wrong. Please reload the page and try again.',
                'context': {}
            }
    def start(self):
        start_param = 'hjukwkJIgAlPEUHd'
        wapi_response = self.wapi.get_response(start_param, {})
        if('output' in wapi_response and 'context' in wapi_response):
            text = wapi_response['output']['text'][0]
            context = wapi_response['context']
            return {
                'text': text,
                'context': context
            }
        else:
            return {
                'text': 'Something went wrong. Please reload the page and try again.',
                'context': {}
            }

    def convert_to_arabic(self, response):
        response['text'] = self.gapi.convert_to_arabic(response['text'])
        return response
