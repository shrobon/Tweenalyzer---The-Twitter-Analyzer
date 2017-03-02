#__Author__ : Shrobon Biswas

#__Description__:
#This script will use twitter api
#The necessary data will be returned to the server for parsing 
#The script will just accept the Query String

import tweepy
import numpy as np
import configurations 
import pandas as pd

def QueryTwitter(search_string):
	
	#Fetching the Configuration Settings
	key = configurations.consumer_key
	secret = configurations.consumer_secret

	#Authenticating ::
	#------Receiving Access Tokens
	access_token = tweepy.OAuthHandler(consumer_key=key,consumer_secret=secret)
	#------Instantiating the API with our Access Token
	api = tweepy.API(access_token)

	results = api.search(q=search_string)
	return len(results)


