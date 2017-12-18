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

	def start_query(self,query):
		'''
			TODO : SPEPARATE EACH SECTION INTO A FUNCTION
			limit every function in 25 lines
		'''

		#request starts here ---- SECTION ----
		'''
			TODO:
				ADD A SECTION FOR self.gmaps.direction with TRANSIT MODE and AVOIDS
		'''
		extracted_info = self.begin_extract_info(query)
		try:
			direction_results = self.gmaps.directions(extracted_info[0],extracted_info[1])
			log(str(direction_results) + "\n")

			if len(direction_results) < 0:
				return None

			result_info_payload,result_info_steps = self.get_primary_info(direction_results)
			
			return self.get_steps(result_info_steps,result_info_payload)
		
		except Exception as e:
			log(e)
			return None

	def get_primary_info(self,direction_results):
		for direction_result in direction_results:
			for leg_info in direction_result['legs']:
				start_loc = leg_info['start_address']
				end_loc = leg_info['end_address']
				end_latlng = leg_info['end_location']
				distance = leg_info['distance']['text']
				time = leg_info['duration']['text']
				transit_mode = leg_info['steps'][0]['travel_mode']
				steps = leg_info['steps']


		response_payload = [{
		'title': start_loc + ' to ' + end_loc,
		'subtitle' : 'Distance :' + str(distance) + '\nTravel time : ' + str(time) + '\nTravel mode :' + transit_mode,
		'image_url' : 'https://maps.googleapis.com/maps/api/staticmap?&key={}&center={}&zoom=13&size=450x250&maptype=roadmap&format=jpg'.format(self.gapikey,str(end_latlng['lat'])+','+str(end_latlng['lng']))
		}]

		return (response_payload,steps)
	
	def get_steps(self,steps,original_payload):
		for step in steps:
			additional_instruction = {
				'title' : step['html_instructions'].replace('<b>','').replace('</b>','').replace('<div style="font-size:0.9em"','').replace('</div>',''),
				'subtitle' : 'Distance :' + str(step['distance']['text']) + '\nTravel time : ' + str(step['duration']['text']),
				'image_url' : 'https://maps.googleapis.com/maps/api/staticmap?&key={}&center={}&zoom=13&size=450x250&maptype=roadmap&format=jpg'.format(self.gapikey,str(step['end_location']['lat'])+','+str(step['end_location']['lng']))
			}
			
			original_payload.append(additional_instruction)

		return original_payload
	
	def begin_extract_info(self,query):
		#data extraction starts here ---- SECTION ----
		'''
			TODO:
				extract transit modes,and avoids
		'''
		if 'far' in query or 'long' in query or 'distance' in query or 'time' in query:
			base_query = csv_reader('distancetime.csv')
		else:
			base_query = csv_reader('direction.csv')

		extracted_info = extract_info(base_query,query)
		#reverse the TO and FROM if 'TO' comes first
		if query.find('to') > query.find('from'):
			extracted_info[0],extracted_info[1] = extracted_info[1],extracted_info[0]
		
		log("inf : " + str(extract_info(base_query,query)))

		return extracted_info