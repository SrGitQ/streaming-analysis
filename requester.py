import functions_framework
import re
import requests
from textblob import TextBlob

class Analytics:
	def __init__(self, data = None, tweet = None):
		self.hashtag = data['hashtag'] if data else tweet['topic']
		self.tweets = data['tweets'] if data else 1
		self.users = data['users'] if data else [tweet['user_screen_name']]
		self.no_users = data['no_users'] if data else 1
		self.mentions = data['mentions'] if data else tweet['tweet_text'].count('@')
		self.places = data['places'] if data else 1 if tweet['user_loc_code'] else 0
		self.verified = data['verified'] if data else 1 if tweet['user_verified'] else 0
		self.raw = data['raw'] if data else [tweet]
		
		
		if data:
			self.sentiment = data['sentiment']
			self.sentiment_avg = data['sentiment_avg']
		else:
			self.sentiment = {
				"positive": 0,
				"neutral": 0,
				"negative": 0,
			}
			
			self.sentiment[self.calculate_sentiment(tweet['tweet_text'])] += 1 
			self.sentiment_avg = {
				"positive": (self.sentiment['positive']) / self.no_users,
				"neutral": (self.sentiment['neutral']) / self.no_users,
				"negative": (self.sentiment['negative']) / self.no_users,
			}


		self.devices = data['devices'] if data else {'android': 0, 'ios': 0, 'web': 0}
		if not data:
			self.devicesCounter(tweet['source'])

		self.sentiment_timeline = data['sentiment_timeline'] if data else [self.sentiment]

		if data and 'hash_network' in data:
			self.hash_network = data['hash_network']
		elif tweet and 'tweet_text' in tweet:
			self.hash_network = self.get_hash_network(tweet['tweet_text'])
		
		self.hashtags = data['hashtags'] if data else tweet['tweet_text'].count('#')
		self.places_locations = data['places_locations'] if data else [{'lat':tweet['user_lat'], 'lng':tweet['user_lon']}]
	
	def calculate_sentiment(self, text):
		sentiment = TextBlob(text).sentiment.polarity
		return 'positive' if sentiment > 0 else 'negative' if sentiment < 0 else 'neutral'
	
	def get_device(self, source):
		if 'Android' in source:
			return "android"
		elif 'iPhone' in source or 'ios' in source:
			return "ios"
		else:
			return "web"
	
	def devicesCounter(self, source):
		device = self.get_device(source)
		self.devices[device] += 1

	def get_hash_network(self, text):
		hashtags = re.findall(r'#\w+',text.lower())
		nodes = []
		links = []
		for hashtag in hashtags:
			nodes.append({"id": hashtag})
		if self.hashtag not in hashtags:
			hashtags.append(self.hashtag)
		for i in range(len(hashtags)):
			for j in range(i+1, len(hashtags)):
				links.append({"source": hashtags[i], "target": hashtags[j]})
		return {"nodes": nodes, "links": links}
	
	def __dict__(self):
		return {
			"hashtag": self.hashtag,
			"tweets": self.tweets,
			"users": self.users,
			"no_users": self.no_users,
			"mentions": self.mentions,
			"places": self.places,
			"verified": self.verified,
			"raw": self.raw,
			"sentiment": self.sentiment,
			"sentiment_avg": self.sentiment_avg,
			"devices": self.devices,
			"sentiment_timeline": self.sentiment_timeline,
			"hash_network": self.hash_network if self.hash_network else {"nodes": [], "links": []},
			"hashtags": self.hashtags,
			"places_locations": self.places_locations,
		}
	
	def add_tweet(self, tweet):
		self.tweets += 1
		if tweet['user_screen_name'] not in self.users:
			self.users.append(tweet['user_screen_name'])
			self.no_users += 1
		self.mentions += tweet['tweet_text'].count('@')
		self.places += 1 if tweet['user_loc_code'] else 0
		self.verified += 1 if tweet['user_verified'] else 0
		self.raw.append(tweet)

		self.sentiment[self.calculate_sentiment(tweet['tweet_text'])] += 1
		self.sentiment_avg = {
			"positive": (self.sentiment['positive']) / self.no_users,
			"neutral": (self.sentiment['neutral']) / self.no_users,
			"negative": (self.sentiment['negative']) / self.no_users,
		}

		self.sentiment_timeline.append(self.sentiment)
		self.devicesCounter(tweet['source'])
		self.hashtags += tweet['tweet_text'].count('#')
		self.places_locations.append({'lat':tweet['user_lat'], 'lng':tweet['user_lon']})
		try:
			new_connections = self.get_hash_network(tweet['tweet_text'])
			nodes = self.hash_network['nodes']
			for node in new_connections['nodes']:
				if node not in nodes:
					nodes.append(node)
			links = self.hash_network['links']
			for link in new_connections['links']:
				if link not in links:
					links.append(link)
			self.hash_network = { 'nodes': nodes, 'links': links }
		except:
			Exception("Error handlening from hash network none of type")

@functions_framework.http
def entry(request):
	"""HTTP Cloud Function.
	Args:
	    request (flask.Request): The request object.
	    <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
	Returns:
	    The response text, or any set of values that can be turned into a
	    Response object using `make_response`
	    <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
	"""
	request_json = request.get_json(silent=True)
	topic = request_json['topic']
	current = requests.get('https://twitter-streaming-365514-default-rtdb.firebaseio.com/'+topic+'.json').json()

	if current:
		id = list(current.keys())[0]
		current_analysis = Analytics(current[id])
		current_analysis.add_tweet(request_json)
		requests.put('https://twitter-streaming-365514-default-rtdb.firebaseio.com/'+topic+'.json', json={id:current_analysis.__dict__()})
	else:
		current_analysis = Analytics(None, request_json)
		requests.post('https://twitter-streaming-365514-default-rtdb.firebaseio.com/'+topic+'.json', json=current_analysis.__dict__())

	return 'Hello !'
