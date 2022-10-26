import tweepy
from tweepy import Stream
from google.cloud import pubsub_v1
import datetime
import os
import json
from geopy.geocoders import Nominatim
import base64
import requests


# #READ CREDENTIALS AND USER PROFILE
# config=open("twitter-config.txt","r")
# lines=config.readlines()
# api_key=lines[0].split("api_key=")[1].replace("\n","")
# api_key_secret=lines[1].split("api_key_secret=")[1].replace("\n","")
# access_token=lines[2].split("access_token=")[1].replace("\n","")
# access_token_secret=lines[3].split("access_token_secret=")[1].replace("\n","")
# config.close()

# # SETTING THE AUTH FOR GCP PROJECT ENVIRONMENT
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='twitter-streaming-365514-e2b15f524bb2.json'

# # INITIALIZE NOMINATIM API
geolocator = Nominatim(user_agent="MyApp")

# PUBISHING TWEETS
def publish(client, pubsub_topic, data_lines):
    """Publish to the given pubsub topic."""
    messages = []

    for line in data_lines:
        messages.append({'data': line})

    body = {'messages':messages}

    str_body = json.dumps(body)
    data_encoded = str_body.encode("utf-8")
    pubsub_message = data_encoded.decode('utf-8', 'replace')
    #data = base64.urlsafe_b64encode(bytearray(str_body, 'utf8'))
    #data = base64.urlsafe_b64encode(bytearray(body, 'utf8'))
    #pubsub_message = base64.urlsafe_b64decode(data).decode('utf-8')
    
    print(type(data_encoded),data_encoded,'\n')
    client.publish(topic=pubsub_topic, data=data_encoded)
    print(type(pubsub_message),pubsub_message,'\n\n')


# LISTENER CLASS
class Listener(Stream):

	# client = None#pubsub_v1.PublisherClient()
	topic = None

	tweets = []
	batch_size = 1
	total_tweets = 1000
	count = 0

	# def write_to_pubsub(self, tweets):
	# 	self.pubsub_topic = self.client.topic_path("twitter-streaming-365514", "example")
	# 	publish(self.client, self.pubsub_topic, tweets)

	def on_status(self, status):
		ruled = requests.get('http://localhost:5000/stream_ruled').json()['ruled']
		if not ruled:
			self.disconnect()

		# User information
		user_name = status.user.name
		user_screen_name = status.user.screen_name
		user_followers = status.user.followers_count
		user_friends = status.user.friends_count
		user_loc = status.user.location	
		try:
			user_loc_lat_lon = geolocator.geocode(user_loc)
		except:
			user_loc_lat_lon = 'California USA'	
		if type(user_loc_lat_lon) == type(None):
			user_lat =  "44.933143"
			user_long = "7.540121"
		else:
			user_lat =  str(user_loc_lat_lon.latitude)
			user_long = str(user_loc_lat_lon.longitude)	
		user_bio = status.user.description
		user_verified = status.user.verified	
		# Tweet details
		created_at = status.created_at.isoformat()
		id_str = status.id_str
		text = status.text
		source = status.source
		tweet_like_count = status.favorite_count
		tweet_reply_count = status.retweet_count

		# Creating a new tweet dict
		new_tweet = {'tweet_id':id_str,
					'topic':self.topic,
		            'user_name':user_name,
		            'user_screen_name':user_screen_name,
		            'user_followers':user_followers,
		            'user_friends': user_friends,
		            'user_loc_code': user_loc,
		            'user_lat': user_lat,
		            'user_lon': user_long,
		            'user_bio': user_bio,
		            'user_verified': user_verified,
		            'tweet_text': text,
		            'created_at':created_at,
		            'tweet_like_count': tweet_like_count,
		            'tweet_reply_count': tweet_reply_count,
		            'source': source}	
		requests.post('https://function-3-iy4drk2okq-ue.a.run.app', json=new_tweet)
		# Appending dict to the list
		# self.tweets.append(new_tweet)	
		# # Verifiying the size of the batch
		# if len(self.tweets) >= self.batch_size:
		# 	# Pubishing the twet
			
		# 	# self.write_to_pubsub(self.tweets)

		# 	self.tweets = []	
		self.count += 1
		if self.count >= self.total_tweets:
			return False	
		if (self.count % 5) == 0:
			print("count is: {} at {}".format(self.count, datetime.datetime.now()))
        

# if __name__ == '__main__':

#     stream_tweet = Linstener(api_key, api_key_secret, access_token, access_token_secret)
	
#     keywords = ['Shakira']
#     stream_tweet.filter(track=keywords,languages=['es'])
