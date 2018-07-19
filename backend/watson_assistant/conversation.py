from .watson import WatsonAPI
from .zomato import ZomatoAPI
from pprint import pprint

class Conversation():
    def __init__(self):
        self.wapi = WatsonAPI()
        self.zapi = ZomatoAPI()
        pass

    def locate_restaurant(self, params, context, result):
        # TODO: Implement actual zomato search, or build restaurant DB
        restaurant_data = self.zapi.find_restaurant_by_cuisine(params, context)
        context[result] = restaurant_data
        return context

    def find_route(self, params, context, result):
        restaurant = None
        if 'restaurant' in params:
            restaurant = params['restaurant']
        elif 'restaurant' in context:
            restaurant = context['restaurant']
        route = {
            'time': '24 minutes',
            'details': 'Get out.'
        }
        context[result] = route
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
                'exit_chat': self.exit_chat
            }
            switcher_result = {
                'context.restaurant': 'restaurant',
                'context.route': 'route',
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
            pprint(wapi_response)
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