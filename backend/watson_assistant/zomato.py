import json
from pprint import pprint
import requests
# from models import Restaurant

        

class ZomatoAPI():
    def __init__(self):
        with open('config.json') as f:
            self.config = json.load(f)['zomato']
        with open('data.json') as f:
            self.data = json.load(f)
    
    def location_details(self, entity_id, entity_type):
        # Build URL base and headers
        url = self.config['base_url']
        url += self.config['location_details']
        headers = {
            'Accept': 'application/json',
            'user-key': self.config['key']
        }

        # Custom changes
        entity_type = entity_type.replace(' ', '')
        url = url.replace('<entity_id>', str(entity_id), 1)
        url = url.replace('<entity_type>', entity_type, 1)

        # Response handling
        response = requests.get(url, headers=headers)
        response_data = json.loads(response.text)
        pprint(response_data)
        restaurants = []
        # pprint(response_data)
        for x in response_data['best_rated_restaurant']:
            restaurants.append( Restaurant(x['restaurant']) )
        return restaurants


    def locations(self, location):
        # Build URL base and headers
        url = self.config['base_url']
        url += self.config['locations']
        headers = {
            'Accept': 'application/json',
            'user-key': self.config['key']
        }

        # Custom changes
        location = location.replace(' ', '%20')
        url = url.replace('<location>', location, 1)

        # Response handling
        response = requests.get(url, headers=headers)
        location_entity = None
        response_data = json.loads(response.text)
        for loc in response_data['location_suggestions']:
            if(loc['city_name'] == 'Dubai'):
                location_entity = loc
                break

        if(not location_entity):
            return "I'm sorry, I can only find locations in Dubai. Exiting now."
            # exit(0)
        response = dict()
        response['entity_id'] = location_entity['entity_id']
        response['entity_name'] = location_entity['title']
        response['entity_type'] = location_entity['entity_type']
        response['lat_long'] = [location_entity['latitude'], location_entity['longitude']]
        return response

    def find_restaurants_by_location(self, location):
        location = self.locations(location)
        rests = self.location_details(location['entity_id'], location['entity_type'])
        return rests

    def find_restaurant_by_cuisine(self, params, context):
        existing = None
        if('restaurant' in context):
            exisiting = context['restaurant']
        for rest in self.data['restaurants']:
            if(rest['cuisine'] == params['cuisine']):
                restaurant = {
                    'name': rest['name'],
                    'address': rest['address']
                }
                if(existing != None and restaurant == existing):
                    continue
                return restaurant
        restaurant = {
            'found': 'not found'
        }
        return restaurant
        