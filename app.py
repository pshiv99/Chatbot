from flask import Flask, request
app = Flask(__name__)

verify_token = 'abcd'

@app.route('/webhook', methods = ['GET'])
def index():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode and token:
        if mode == 'subscribe' and token == verify_token:
            print('WEBHOOK_VERIFIED')
            return challenge