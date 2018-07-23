import googlemaps
from datetime import datetime
import json
import os
from pprint import pprint

class GoogleAPI():
    def __init__(self):
        self.key = os.getenv('GOOGLE_KEY')
        self.gmaps = googlemaps.Client(key=self.key)

    def find_restaurant(self, context, cuisine):

        if 'restaurant' in context and 'cuisine' in context['restaurant']:
            print("Context: ")
            pprint(context)
            if cuisine == context['restaurant']['cuisine']:

                origin = context['latlong']
                destination = context['restaurant']['latlong']
                now = datetime.now()
                directions_result = self.gmaps.directions(origin,
                                        destination,
                                        departure_time=now)

                distance = directions_result[0]['legs'][0]['distance']['text']
                distance, unit = distance.split(' ')
                distance = float(distance)
                print("Reached googleAPI distance: ", distance)
                print(unit)
                if unit == 'km':
                    distance = distance * 1000
                distance = distance + (1000-distance)%1000
                if 'bias' in context['restaurant']:
                    distance = int(context['restaurant']['bias']) + 1000
                print("Reached googleAPI calculate distance: ", distance)
                while distance <= 10000:
                    print("Reached googleAPI distance loop")
                    query = cuisine + ' restaurant'
                    location = 'circle:' + str(int(distance)) + '@' + origin
                    print("location_bias: ", location)
                    google_result = self.gmaps.find_place(query, 'textquery', fields=['geometry', 'id', 'name', 'photos', 'place_id', 'formatted_address'],
                                            location_bias=location,
                                            language='en-US')
                    pprint(google_result)
                    candidate = google_result['candidates'][0]

                    if candidate['place_id'] != context['restaurant']['place_id']:
                        loc = candidate['geometry']['location']
                        latlong = str(loc['lat']) + ',' + str(loc['lng'])
                        return {
                            'place_id': candidate['place_id'],
                            'name': candidate['name'],
                            'cuisine': cuisine,
                            'address': candidate['formatted_address'],
                            'latlong': latlong,
                            'bias': distance
                        }
                    else:
                        distance += 1000
                else:
                    return {
                        'found': 'not found'
                    }
            else:
                query = cuisine + ' restaurant'
                location = 'point:' + context['latlong']
                google_result = self.gmaps.find_place(query, 'textquery', fields=['geometry', 'id', 'name', 'photos', 'place_id', 'formatted_address'],
                                        location_bias=location,
                                        language='en-US')
                candidate = google_result['candidates'][0]
                loc = candidate['geometry']['location']
                latlong = str(loc['lat']) + ',' + str(loc['lng'])
                return {
                    'place_id': candidate['place_id'],
                    'name': candidate['name'],
                    'address': candidate['formatted_address'],
                    'cuisine': cuisine,
                    'latlong': latlong
                }
        else:
            query = cuisine + ' restaurant'
            location = 'point:' + context['latlong']
            google_result = self.gmaps.find_place(query, 'textquery', fields=['geometry', 'id', 'name', 'photos', 'place_id', 'formatted_address'],
                                    location_bias=location,
                                    language='en-US')
            candidate = google_result['candidates'][0]
            loc = candidate['geometry']['location']
            latlong = str(loc['lat']) + ',' + str(loc['lng'])
            return {
                'place_id': candidate['place_id'],
                'name': candidate['name'],
                'address': candidate['formatted_address'],
                'cuisine': cuisine,
                'latlong': latlong
            }

    def find_route(self, context):
        origin = context['latlong']
        destination = context['restaurant']['latlong']
        now = datetime.now()
        directions_result = self.gmaps.directions(origin,
                                destination,
                                departure_time=now)
        duration = directions_result[0]['legs'][0]['duration']['text']
        distance = directions_result[0]['legs'][0]['distance']['text']
        time = duration + "(" + distance + ")"
        return {
            'time': time
        }

    def find_url(self, context):
        base_url = 'https://www.google.com/maps/dir/?api=1&'
        static_url = 'https://maps.googleapis.com/maps/api/staticmap?'
        static_url += 'center=&zoom=13&scale=1&size=150x100&maptype=roadmap&key=' + os.getenv('GOOGLE_STATIC_KEY') + '&format=png&visual_refresh=true'
        static_url += '&markers=size:mid|color:0x10ff4a|label:0|' + context['restaurant']['latlong']
        origin = 'origin=' + context['latlong']
        destination = 'destination=' + context['restaurant']['latlong']
        url = base_url + origin + '&' + destination
        link = '<a target=_blank href="' + url + '"><img src="' + static_url + '"></a>'
        return {
            'link': link
        }

    def convert_to_arabic(self, text):
        pass
