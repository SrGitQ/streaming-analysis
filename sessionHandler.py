import requests
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
from google.cloud import pubsub_v1
import threading
import time
import os
from tweets_scrapper import Listener
from geopy.geocoders import Nominatim
from keys import *

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='twitter-streaming-365514-e2b15f524bb2.json'
print('Credendtials from environ: {}'.format(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')))
client = pubsub_v1.PublisherClient()

app = Flask(__name__)
cors = CORS(app)
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")
app.config['CORS_HEADERS'] = 'Content-Type'

# stream_tweet = Listener(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# Listener.client = client
# keywords = ['HouseTargaryen']
# stream_tweet.topic = 'HouseTargaryen'
# stream_tweet.filter(track=keywords, languages=['en'])

# geolocator = Nominatim(user_agent="MyApp")

default_data = {
	"hashtag": "hashtag",
	"tweets": 140,
	"users": 140,
	"mentions": 13,
	"places": 13,
	"no_users": 13,
	"verified": 13,
	"sentiment": {
		"positive": 0.60,
		"neutral": 0.20,
		"negative": 0.20,
	},
	"devices": {
		"android": 33,
		"ios": 36,
		"web": 33,
	},
	"sentiment_timeline": [
		{ "positive": 0.33, "neutral": 0.53, "negative": 0.33 },
		{ "positive": 0.3, "neutral": 0.53, "negative": 0.33 },
		{ "positive": 0.23, "neutral": 0.33, "negative": 0.60 },
		{ "positive": 0.12, "neutral": 0.33, "negative": 0.33 },
		{ "positive": 0.6, "neutral": 0.20, "negative": 0.20 },
	],
	"hash_network":{
			"nodes": [
				{ "id": '#Harry' },
				{ "id": '#Potter' },
				{ "id": '#Sally' },
			],
			"links": [
				{ "source": '#Harry', "target": '#Sally' },
				{ "source": '#Potter', "target": '#Sally' },
				{ "source": '#Harry', "target": '#Potter' },
			]
	},
	"hashtags": 140,
	"places_locations":[
		{ "lat": 21.009293505988, "lng": -89.69595640433737},
		{ "lat": 20.009293505988, "lng": -88.69595640433737},

	]
}
trusted_hash = ''

i = 0

connected = False

@app.route('/streamdata')
@cross_origin()
def incrementHandler():
	global connected
	global default_data
	global trusted_hash
	try:
		if trusted_hash != '':
			print('debbuging flag 2',trusted_hash)
			under_condition_data = requests.get(f'https://twitter-streaming-365514-default-rtdb.firebaseio.com/{trusted_hash}.json').json()
			under_condition_data = list(under_condition_data.values())[0]
			default_data = under_condition_data
		return default_data
	except:
		return default_data

@cross_origin()
@socketio.on('connect')
def connect(auth):
	global connected
	socketio.emit('currentStatus', {'data': 'Connected'})
	connected = True
	thread = threading.Thread(target=incrementHandler)
	thread.start() 


@cross_origin()
@socketio.on('disconnect')
def disconnect():
	global i
	global connected
	print('Client disconnected')
	i = 0
	connected = False

@cross_origin()
@app.route('/')
def index():
	return 'Hello World!'

def stream_runner(hash:str):
	stream_tweet = Listener(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	keywords = [hash]
	stream_tweet.topic = hash
	stream_tweet.filter(track=keywords, languages=['en','es'])

@cross_origin()
@app.route('/stream_ruled')
def stream_ruled():
	global connected
	return {"ruled": connected}

@cross_origin()
@app.route('/stop')
def stop():
	global connected
	connected = False

	return 'stopped'


@cross_origin()
@app.route('/hashtag/<hash>')
def hashtag_getter(hash):
	global connected
	global trusted_hash
	trusted_hash = hash
	connected = True
	thread = threading.Thread(target=stream_runner, args=(hash,))
	thread.start()
	return hash
