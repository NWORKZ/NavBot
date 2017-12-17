from utils import log,send_list
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
						if 'go' in rcv_msg:#to be deleted
							#please wait message
							messenger_bot.send_text_message(sender,"Okay! Please wait I am looking it up now.")
							if gmaps.get_direction(rcv_msg) is not None:
								#messenger_bot.send_generic_message(sender,gmaps.get_direction(rcv_msg))
								send_list(facebook_PAT,sender,gmaps.get_direction(rcv_msg))
							else:
								messenger_bot.send_text_message(sender,"I can't find any routes for that")
						else:
							messenger_bot.send_text_message(sender,'wrong keyword')#to be deleted
					else:						
						messenger_bot.send_text_message(sender,"Sorry, I don't understand that")

	return 'ok', 200


if __name__ == '__main__':
	app.run(debug = True, port = 80)