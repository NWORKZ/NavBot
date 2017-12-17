from utils import extract_info, csv_reader, log
import re
import json
import googlemaps

class Maps:
	"""	Maps return a result from a request base on the destination and origin

		Attributes: 
			api_key - Google map api key
	"""

	def __init__(self, api_key):
		self.gapikey = api_key
		self.gmaps = googlemaps.Client(key = api_key)

	def get_direction(self,query):
		direction_results = self.gmaps.directions('tanuan','malvar')
				
		for direction_result in direction_results:
			for leg_info in direction_result['legs']:
				start_loc = leg_info['start_address']
				end_loc = leg_info['end_address']
				end_latlng = leg_info['end_location']
				distance = leg_info['distance']['text']
				time = leg_info['duration']['text']
				transit_mode = leg_info['steps'][0]['travel_mode']
				#clean the instruction of html formatting
				#or make this as a button with next and previous
				instruction = [ins['html_instructions'].replace('<b>','').replace('</b>','').replace('<div style="font-size:0.9em"','').replace('</div>','') for ins in leg_info['steps']]
		
		img_url = 'https://maps.googleapis.com/maps/api/staticmap?&key={}&center=lipa&zoom=13&size=450x250&maptype=roadmap&format=jpg'.format(self.gapikey,str(end_latlng['lat'])+','+str(end_latlng['lng']))
		response_payload = [{
		'title': start_loc + ' to ' + end_loc,
		'subtitle' : 'Distance :' + str(distance) + '\nTravel time : ' + str(time) + '\nTravel mode :' + transit_mode,
		'image_url' : img_url
		}]

		return response_payload
		