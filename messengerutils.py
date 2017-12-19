import requests
from utils import log

class Botc:

	def __init__(self,PAT):
		self.access_token = PAT

	def send_list_large(self,receiver,elements):
		try:
			payload = {
				'message':{
					'attachment' : {
						'type' : 'template',
						'payload' : {
						'template_type' : 'list',
						'top_element_style' : 'large',
						'elements': elements
						}
					}
				}
			}
			payload['recipient'] = {'id' : receiver}
			r = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token='+self.access_token, json = payload)
			log(r.text)
			log('sent')
		except Exception as e:
			log(e)

	def send_list_compact(self,receiver,elements):
		try:
			payload = {
				'message':{
					'attachment' : {
						'type' : 'template',
						'payload' : {
						'template_type' : 'list',
						'top_element_style' : 'compact',
						'elements': elements
						}
					}
				}
			}
			payload['recipient'] = {'id' : receiver}
			r = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token='+self.access_token, json = payload)
		except Exception as e:
			log(e)		

	def mark_seen(self,receiver):
		try:
			payload = {
				'sender_action' : 'mark_seen'
			}
			
			payload['recipient'] = {'id' : receiver}
			r = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token='+self.access_token, json = payload)
		except Exception as e:
			log(e)

	def show_typing(self,receiver):
		try:
			payload = {
				'sender_action' : 'typing_on'
			}
			
			payload['recipient'] = {'id' : receiver}
			r = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token='+self.access_token, json = payload)
		except Exception as e:
			log(e)

	def hide_typing(self,receiver):
		try:
			payload = {
				'sender_action' : 'typing_off'
			}
			
			payload['recipient'] = {'id' : receiver}
			r = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token='+self.access_token, json = payload)
		except Exception as e:
			log(e)	