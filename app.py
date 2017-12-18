from utils import log,send_list_large,send_list_compact
from flask import Flask, request
from pymessenger.bot import Bot
from maps import Maps

app = Flask(__name__)

facebook_PAT = 'EAAFWsHcePX8BALl1ZA0o15A1IdGqhkqzZCUQtIG34CVQJZBrMCHZAJYUZBoB24xPWkfPYFawVms4fMzPPLpeRI1mjnhAsSqZCdYqcQlNuwXpLkZCA71vfE6g9hExv9o8txmZCZA63HfpclSrwKDrlogH55KDZA8RnMZBTRMf4KBmEiuzZBQQAUXFG88G'
facebook_verify_token = 'verify_me'
google_api_key = 'AIzaSyBCWB1CSipmOAoSiPCSM7f7jrbSYqdqvcs'

messenger_bot = Bot(facebook_PAT)
gmaps = Maps(google_api_key)

@app.route('/', methods=['GET'])
def verify_webhook():
	if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
		if not request.args.get('hub.verify_token') == facebook_verify_token:
			return 'Webhook token mismatch', 403
		return request.args['hub.challenge'], 200
	return 'You Reach the webhook', 200

@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	if data['object'] == 'page':
		for msg_entry in data['entry']:
			for msging_detail in msg_entry['messaging']:
				sender = msging_detail['sender']['id']

				if 'message' in msging_detail:
					message_details = msging_detail['message']
					if 'text' in message_details:
						#insert the query processing here
						rcv_msg = message_details['text'].lower()
						#add a tripple dot here for typing
						response = gmaps.start_query(rcv_msg)
						send_response(sender,response)
					else:						
						messenger_bot.send_text_message(sender,"Sorry, I don't understand that")

	return 'ok', 200

def send_response(receiver,response):
	if response is not None:
		log(len(response))
		if len(response) <= 4:
			send_list_large(facebook_PAT,receiver,response)
		else:
			index = 0
			while index < len(response):
				if index == 0:
					send_list_large(facebook_PAT,receiver,response[index:index+4])
				elif index - len(response) == 1:
					messenger_bot.send_genic_message(receiver,response[-1])
				else:
					send_list_compact(facebook_PAT,receiver,response[index:index+4])
				index = index + 3	
	else:
		messenger_bot.send_text_message(receiver,"I can't find any routes for that")

if __name__ == '__main__':
	app.run(debug = True, port = 80)