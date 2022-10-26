from google.cloud import bigquery
from google.oauth2 import service_account
from geopy.geocoders import Nominatim

import os
import pandas as pd
import json
import numpy as np
import datetime as datetime

import warnings
warnings.simplefilter("ignore")


def preparation(df_bq):
	list_=[]
	for i in range(len(df_bq)):
		value= "{},{}".format(df_bq.iloc[i]['user_lat'], df_bq.iloc[i]['user_lon'])
		list_.append(value)
	df_bq['zone']= list_	
	df_bq['created_at'] =  pd.to_datetime(df_bq['created_at'], infer_datetime_format=True)	
	return df_bq

def Auth(sql):
	bq_cred= service_account.Credentials.from_service_account_file('gcp-bigquery/twitter-streaming-365514-4dd6c93453b9.json')
	df_bq= pd.read_gbq(sql, project_id='twitter-streaming-365514', credentials= bq_cred, dialect='standard')
	df_bq= preparation(df_bq)
	return df_bq

def top_countries(top_10_places_dict):
	listCoord= list(top_10_places_dict.keys())
	geolocator = Nominatim(user_agent="geoapiExercises")
	list_countries=[]
	for i in range(len(listCoord)):
		value= listCoord[i]
		location = geolocator.reverse(value)
		address = location.raw['address']
		country = address.get('country', '')
		list_countries.append(country)	
	final_dict = dict(zip(list_countries, list(top_10_places_dict.values())))
	return final_dict

def statistic_response (df_bq):
	user= len(df_bq["user_name"].value_counts().index)
	tweets= len(df_bq["tweet_id"].value_counts().index)	
	#df_bq["tweet_reply_count"].value_counts().index
	df_bq["tweet_reply_count"].value_counts()
	places= len(df_bq["zone"].value_counts().index)	
	top_10_places= df_bq["zone"].value_counts()
	top_10_places_dict= top_10_places[:3].to_dict()
	top_10_places_dict= top_countries(top_10_places_dict)	
	user_verified= df_bq["user_verified"].value_counts()
	user_verified= user_verified[1]	
	top_sources= df_bq["source"].value_counts()
	top_sources = top_sources[:3].to_dict()	
	time_w_freq= df_bq["created_at"].value_counts()
	time_count= time_w_freq.to_dict()	
	aggregation = {'cnt': ('tweet_id', 'count')}
	sentiment_by_time = df_bq.groupby(['created_at', 'sentiment_label']).agg(**aggregation).reset_index().to_dict()	
	dict_statistic= {'Total_tweets': tweets, 'Total_user': user, 'Total_replies':0, 'Total_places': places, 'Top_places': [top_10_places_dict], 'Total_verified_people': user_verified, 
	                    'Top_user_sources':top_sources,'Time_frecuency': time_count, 'Time_frecuency_sentiment': sentiment_by_time }
	return dict_statistic

sql= "SELECT * FROM `twitter-streaming-365514.tweets_tracking.shakira_table` LIMIT 10"
df_bq= Auth(sql)
df_bq.head(2)
