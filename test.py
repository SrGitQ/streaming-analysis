from textblob import TextBlob
import requests
default_data = {
	"hashtag": "hashtag",
	"tweets": 140,
	"users": 140,
	"mentions": 13,
	"places": 13,
	"verified": 13,
	"raw":[
		{"data": {"tweet_id": "1584280140476866561", "user_name": "luuu", "user_screen_name": "luureyes_lu", "user_followers": 6, "user_friends": 206, "user_loc_code": None, "user_lat": "44.933143", "user_lon": "7.540121", "user_bio": "awdawdawdaw", "user_verified": False, "tweet_text": "awdawd", "created_at": "2022-10-23T20:26:34+00:00", "tweet_like_count": 0, "tweet_reply_count": 0, "source": "Twitter for Android", "topic":"hashtag"}}
	],
	"sentiment": {
		"positive": 0.60,
		"neutral": 0.20,
		"negative": 0.20,
	},
	"devices": {
		"android": 33,
		"ios": 33,
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
				{ "id": '#Sally' },
				{ "id": '#Alice' },
				{ "id": '#Bob' },
			],
			"links": [
				{ "source": '#Harry', "target": '#Sally' },
				{ "source": '#Harry', "target": '#Alice' },
				{ "source": '#Harry', "target": '#Bob' },
			]
	},
	"hashtags": 140,
	"places_locations":[
		{ "lat": 21.009293505988, "lng": -89.69595640433737},
		{ "lat": 20.009293505988, "lng": -88.69595640433737},
		{ "lat": 19.009293505988, "lng": -87.69595640433737},
		{ "lat": 18.009293505988, "lng": -86.69595640433737},

	]
}

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
		self.sentiment = data['sentiment'] if data else self.get_sentiment(tweet['tweet_text'])
		self.devices = data['devices'] if data else {'android': 0, 'ios': 0, 'web': 0}
		self.devicesCounter(tweet['source'])
		self.sentiment_timeline = data['sentiment_timeline'] if data else [self.sentiment]
		self.hash_network = data['hash_network'] if data else self.get_hash_network(tweet['tweet_text'])
		self.hashtags = data['hashtags'] if data else tweet['tweet_text'].count('#')
		self.places_locations = data['places_locations'] if data else [[tweet['user_lat'], tweet['user_lon']]]
	
	def get_sentiment(self, text):
		sentiment = TextBlob(text).sentiment
		return {
			"positive": sentiment.polarity,
			"neutral": 1 - sentiment.polarity,
			"negative": sentiment.subjectivity,
		}
	
	def get_device(self, source):
		if 'Android' in source:
			return "android"
		elif 'iPhone' in source:
			return "ios"
		else:
			return "web"
	
	def devicesCounter(self, source):
		device = self.get_device(source)
		self.devices[device] += 1

	def get_hash_network(self, text):
		hashtags = [hashtag.strip('#') for hashtag in text.split() if hashtag.startswith('#')]
		nodes = []
		links = []
		for hashtag in hashtags:
			nodes.append({"id": hashtag})
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
			"mentions": self.mentions,
			"places": self.places,
			"verified": self.verified,
			"raw": self.raw,
			"sentiment": self.sentiment,
			"devices": self.devices,
			"sentiment_timeline": self.sentiment_timeline,
			"hash_network": self.hash_network,
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

		current = self.get_sentiment(tweet['tweet_text'])


		self.sentiment = {
			"positive": (self.sentiment['positive'] + current['positive']) / len(self.raw),
			"neutral": (self.sentiment['neutral'] + current['neutral']) / len(self.raw),
			"negative": (self.sentiment['negative'] + current['negative']) / len(self.raw),
		}
		self.sentiment_timeline.append(self.sentiment)
		self.devicesCounter(tweet['source'])
		self.hashtags += tweet['tweet_text'].count('#')
		self.places_locations.append([tweet['user_lat'], tweet['user_lon']])
		new_connections = self.get_hash_network(tweet['tweet_text'])
		self.hash_network = { 'nodes':self.hash_network['nodes']+new_connections['nodes'], 'links':self.hash_network['links']+new_connections['links'] }
	


# entry = {"data": {"tweet_id": "1584280140476866561", "user_name": "luuu", "user_screen_name": "luureyes_lu", "user_followers": 6, "user_friends": 206, "user_loc_code": None, "user_lat": "44.933143", "user_lon": "7.540121", "user_bio": "awdawdawdaw", "user_verified": False, "tweet_text": "awdawd #America #ai @hola", "created_at": "2022-10-23T20:26:34+00:00", "tweet_like_count": 0, "tweet_reply_count": 0, "source": "Twitter for Android", "topic":"hashtag"}}

# # different data
# entry_2 = {"data": {"tweet_id": "1584280140476866561", "user_name": "luuu", "user_screen_name": "luureyes_lu", "user_followers": 6, "user_friends": 206, "user_loc_code": None, "user_lat": "44.933143", "user_lon": "7.540121", "user_bio": "awdawdawdaw", "user_verified": True, "tweet_text": "#creacion #lord", "created_at": "2022-10-23T20:26:34+00:00", "tweet_like_count": 0, "tweet_reply_count": 0, "source": "Twitter for ios", "topic":"hashtag"}}

# object = Analytics(tweet=entry['data'])
# print('object created')
# object.add_tweet(tweet=entry_2['data'])
# print('object updated')

# print(object.__dict__())

# requests.post('https://twitter-streaming-365514-default-rtdb.firebaseio.com/America.json', json={'hashtag': 'hashtag', 'tweets': 2, 'users': ['luureyes_lu'], 'mentions': 1, 'places': 0, 'verified': 1, 'raw': [{'tweet_id': '1584280140476866561', 'user_name': 'luuu', 'user_screen_name': 'luureyes_lu', 'user_followers': 6, 'user_friends': 206, 'user_loc_code': None, 'user_lat': '44.933143', 'user_lon': '7.540121', 'user_bio': 'awdawdawdaw', 'user_verified': False, 'tweet_text': 'awdawd #America #ai @hola', 'created_at': '2022-10-23T20:26:34+00:00', 'tweet_like_count': 0, 'tweet_reply_count': 0, 'source': 'Twitter for Android', 'topic': 'hashtag'}, {'tweet_id': '1584280140476866561', 'user_name': 'luuu', 'user_screen_name': 'luureyes_lu', 'user_followers': 6, 'user_friends': 206, 'user_loc_code': None, 'user_lat': '44.933143', 'user_lon': '7.540121', 'user_bio': 'awdawdawdaw', 'user_verified': True, 'tweet_text': '#creacion #lord', 'created_at': '2022-10-23T20:26:34+00:00', 'tweet_like_count': 0, 'tweet_reply_count': 0, 'source': 'Twitter for ios', 'topic': 'hashtag'}], 'sentiment': {'positive': 0.0, 'neutral': 1.0, 'negative': 0.0}, 'devices': {'android': 1, 'ios': 0, 'web': 1}, 'sentiment_timeline': [{'positive': 0.0, 'neutral': 1.0, 'negative': 0.0}, {'positive': 0.0, 'neutral': 1.0, 'negative': 0.0}], 'hash_network': {'nodes': [{'id': 'America'}, {'id': 'ai'}, {'id': 'creacion'}, {'id': 'lord'}], 'links': [{'source': 'America', 'target': 'ai'}, {'source': 'America', 'target': 'hashtag'}, {'source': 'ai', 'target': 'hashtag'}, {'source': 'creacion', 'target': 'lord'}, {'source': 'creacion', 'target': 'hashtag'}, {'source': 'lord', 'target': 'hashtag'}]}, 'hashtags': 4, 'places_locations': [['44.933143', '7.540121'], ['44.933143', '7.540121']]})
data = requests.get('https://twitter-streaming-365514-default-rtdb.firebaseio.com/HouseTargaryen.json').json()
print(list(data.keys())[0])
