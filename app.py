from flask import Flask, request
import json
import requests

app = Flask(__name__)

verify_token = 'abcd'
page_access_token = 'EAAEN94ODDV8BABZAmnrrfTu1DBFr3UQa8h7alxDSyHxunPz22jMYM7sZCyaDkm5PnE2pzZCfbRZBrCuklNSqVAxWgZB5zPhgCPlM9rS2PgtFpb45mAJUAd1kYqhIJYbrgjE0nYTti9ahPfNe2lhGMr076CuzECgHW0qNuX5lhCgZDZD'

@app.route('/webhook')
def index():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == verify_token:
        return challenge

@app.route('/webhook', methods = ['POST'])
def abc():
    data = request.get_json()
    if data['object'] == 'page':
        for entry in data['entry']:
            print(json.dumps(entry['messaging'][0], indent = 2))
        
        sender_psid = entry['messaging'][0]['sender']['id']

        if 'message' in entry['messaging'][0]:
            handleMessage(sender_psid, entry['messaging'][0]['message'])
        elif 'postback' in entry['messaging'][0]:
            handlePostback(sender_psid, entry['messaging'][0]['postback'])

        print(sender_psid)
        return 'EVENT_RECEIVED'

def handleMessage(sender_psid, message):
    if 'text' in message:
        text = message['text']
        payload = {
            'text': f'You sent the message: "{text}". Now send me an image!'
        }
    elif 'attachments' in message:
        attachment_url = message['attachments'][0]['payload']['url']
        payload = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [{
                        'title': 'Is this the right picture?',
                        'subtitle': 'Tap a button to answer.',
                        'image_url': attachment_url,
                        'buttons': [
                            {
                                'type': 'postback',
                                'title': 'Yes!',
                                'payload': 'yes'
                            },
                            {
                                'type': 'postback',
                                'title': 'No!',
                                'payload': 'no',
                            }
                        ]
                    }]
                }
            }
        }
    
    callSendAPI(sender_psid, payload)

def handlePostback(sender_psid, postback):
    payload = postback['payload']
    
    if payload == 'yes':
        response = {
            'text': 'Thanks!'
        }
    elif payload == 'no':
        response = {
            'text': 'Oops, try sending another image.'
        }
    callSendAPI(sender_psid, response)

def callSendAPI(sender_psid, payload):
    request_body = {
        'recipient': {
            'id': sender_psid
        },
        'message': payload
    }

    url = f'https://graph.facebook.com/v2.6/me/messages?access_token={page_access_token}'

    res = requests.post(url, json = request_body)