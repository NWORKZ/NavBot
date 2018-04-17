from utils import extract_info, csv_reader, log
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
		extracted_info = self.begin_extract_info(query)
		try:
			return self.map_request(extracted_info)
		except Exception as e:
			log(e)
			return None

	def map_request(self,extracted_info):
		if extracted_info[1] == 2:
			direction_results = self.gmaps.directions(extracted_info[0][0],extracted_info[0][1])#normal
			if len(direction_results) < 0:
				return None
		elif extracted_info[1] == 3.1:
			#add a synonym words
			direction_results = self.gmaps.directions(extracted_info[0][0],extracted_info[0][1],avoid=extracted_info[0,2])#avoid
			if len(direction_results) < 0:
				return None				
		elif extracted_info[1] == 3.2:
			#add a synonym words
			if extracted_info == 'bike' or extracted_info == 'bicycle':
				direction_results = self.gmaps.directions(extracted_info[0][0],extracted_info[0][1],mode='bicycling')#transit
			else:
				direction_results = self.gmaps.directions(extracted_info[0][0],extracted_info[0][1],mode=extracted_info[0][2])#transit
			if len(direction_results) < 0:
				return None				
		elif extracted_info[1] == 4:
			direction_results = self.gmaps.directions(extracted_info[0][0],extracted_info[0][1],mode=extracted_info[0][2],avoid=extracted_info[0][3])#transit
			if len(direction_results) < 0:
				return None				

		result_info_payload,result_info_steps = self.get_primary_info(direction_results)
		
		return self.get_steps(result_info_steps,result_info_payload)
	
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
		if 'far' in query or 'long' in query or 'distance' in query or 'time' in query:
			base_query = csv_reader('distancetime.csv')
		else:
			base_query = csv_reader('direction.csv')

		if 'how to' in query:
			query = query.replace('how to','')
		elif 'i want to' in query:
			query = query.replace('i want to','')

		extracted_info = extract_info(base_query,query)		
		log("inf : " + str(extract_info(base_query,query)))

		if query.find('to') < query.find('from'):#reverse the TO and FROM if 'TO' comes first
			extracted_info[0],extracted_info[1] = extracted_info[1],extracted_info[0]

		if len(extracted_info) == 4:
			if query.find('avoid') < query.find('by'):#reverse avoid and by of avoid comes first
				extracted_info[2], extracted_info[3] = extracted_info[3], extracted_info[2]
				return [extracted_info,4]
		
		#if only avoid
		if 'avoid' in query and 'by' not in query:
			return [extracted_info,3.1]
		#if only by
		if 'avoid' not in query and 'by' in query:
			return [extracted_info,3.2]

		return [extracted_info,2]