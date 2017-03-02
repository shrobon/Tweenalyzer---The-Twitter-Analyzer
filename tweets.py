#__Author__ : Shrobon Biswas

#__Description__:
#This script will use twitter api
#The necessary data will be returned to the server for parsing 
#The script will just accept the Query String

import tweepy
import numpy as np
import configurations 
import pandas as pd
import time 

#We will be using TextBlob for Sentiment Analysis
from textbblob import TextBlob

'''
This function will help us escape the rate-limit-error we may recieve
'''
def limit_handled(cursor):

    while True:
        try:
        	#time.sleep(1)
        	yield cursor.next()

        except tweepy.RateLimitError:
            time.sleep(30)
            continue

        except StopIteration:
        	break







def QueryTwitter(search_string):

	#Fetching the Configuration Settings
	key = configurations.consumer_key
	secret = configurations.consumer_secret
	access_token = configurations.access_token
	access_secret = configurations.access_secret

	#Authenticating ::
	#Receiving Access Tokens
	auth = tweepy.OAuthHandler(consumer_key=key,consumer_secret=secret)
	auth.set_access_token(access_token, access_secret)

	#Instantiating the API with our Access Token
	api = tweepy.API(auth)

	tweet_list = []
	for tweet in limit_handled(tweepy.Cursor(api.search,q=search_string).items(1000)):
		tweet_list.append(tweet)

	#We now extract details from the tweet and get the resultant DataFrame
	tweet_Data = filter_tweets(tweet_list)


	return len(tweet_list)









# Will be creating the dataframes in this function 
# Snetiment Analysis
def filter_tweets(tweets):
	id_list = [tweet.id for tweet in tweets]
	#Will contain a single column table containing all the tweet ids
	tweet_Data = pd.DataFrame(id_list,columns=['id'])
	tweet_Data["text"] = [tweet.text for tweet in tweets]
	tweet_Data["favourite_count"] = [tweet.favourite_count for tweet in tweets]
	
	#Let us calculate the sentiment scores

	return tweet_Data
