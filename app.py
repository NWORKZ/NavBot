from utils import log
from messengerutils import Botc #custom
from pymessenger.bot import Bot #github
from flask import Flask, request
from maps import Maps

app = Flask(__name__)

facebook_PAT = 'EAAFWsHcePX8BALl1ZA0o15A1IdGqhkqzZCUQtIG34CVQJZBrMCHZAJYUZBoB24xPWkfPYFawVms4fMzPPLpeRI1mjnhAsSqZCdYqcQlNuwXpLkZCA71vfE6g9hExv9o8txmZCZA63HfpclSrwKDrlogH55KDZA8RnMZBTRMf4KBmEiuzZBQQAUXFG88G'
facebook_verify_token = 'verify_me'
google_api_key = 'AIzaSyBCWB1CSipmOAoSiPCSM7f7jrbSYqdqvcs'

messenger_bot = Bot(facebook_PAT)
messenger_bot_c = Botc(facebook_PAT)
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
						messenger_bot_c.mark_seen(sender)
						
						rcv_msg = message_details['text'].lower()
						response = gmaps.start_query(rcv_msg)
						
						messenger_bot_c.show_typing(sender)
						
						send_response(sender,response)
					else:
						messenger_bot_c.mark_seen(sender)						
						messenger_bot_c.show_typing(sender)
						messenger_bot.send_text_message(sender,"Sorry, I don't understand that")
						messenger_bot_c.hide_typing(sender)

	return 'ok', 200

def send_response(receiver,response):
	if response is not None:
		log(len(response))
		if len(response) <= 4:
			messenger_bot_c.send_list_large(receiver,response)
		else:
			index = 0
			while index < len(response):
				if index == 0:
					messenger_bot_c.send_list_large(receiver,response[index:index+4])
				elif index - len(response) == 1:
					messenger_bot.send_genic_message(receiver,response[-1])
				else:
					messenger_bot_c.send_list_compact(receiver,response[index:index+4])
				index = index + 3	
	else:
		messenger_bot.send_text_message(receiver,"I can't find any routes for that")

	messenger_bot_c.hide_typing(receiver)

if __name__ == '__main__':
	app.run(debug = True, port = 80)