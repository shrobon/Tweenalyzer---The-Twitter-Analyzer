#__Author__ : Shrobon Biswas

#__Description__:
#This script will use twitter api
#The necessary data will be returned to the server for parsing 
#The script will just accept the Query String
from __future__ import print_function
import tweepy
import numpy as np
import configurations 
import pandas as pd
import time 
import sys 

#We will be using TextBlob for Sentiment Analysis
#TextBlob is also used for text translation
from textblob import TextBlob
import googlemaps


'''
This function will help us escape the rate-limit-error we may recieve
'''
def limit_handled(cursor):

    while True:
        try:
        	#time.sleep(1)
        	yield cursor.next()

        except tweepy.RateLimitError:
            time.sleep(60*15)
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
	for tweet in limit_handled(tweepy.Cursor(api.search,q=search_string).items(10)):
		tweet_list.append(tweet)

	#We now extract details from the tweet and get the resultant DataFrame
	tweet_Data = filter_tweets(tweet_list)


	return tweet_Data









# Will be creating the dataframes in this function 
# Snetiment Analysis
def filter_tweets(tweets):


	id_list = [tweet.id for tweet in tweets]
	#Will contain a single column table containing all the tweet ids
	tweet_Data = pd.DataFrame(id_list,columns=['id'])
	tweet_Data["text"] = [tweet.text for tweet in tweets]
	#tweet_Data["favourite_count"] = [tweet.favourite_count for tweet in tweets]
	# Location 
	#tweet_Data["location"] = [tweet.author.location for tweet in tweets]



	Sentiments_list = []
	Subjectivity_list = []
	tweet_text_list = []
	tweet_location_list = []
	tweet_lat_lng_list = []


	for tweet in tweets:
		raw_tweet_text = tweet.text
		message = TextBlob(unicode(tweet.text))
		location = tweet.author.location
		# location can be null :: We have to handle that too 
		if len(location) !=0:
			formatted = geocode_location(location)
			tweet_lat_lng_list.append(formatted)
		else:
			tweet_lat_lng_list.append("")




		#Detecting and Changing the language to english
		lang = message.detect_language()

		if lang != u"en":
			message = message.translate(to='en')

		#Changing the Language is important
		#Since it will help in sentiment analysis using TextBlob
		sentiment = message.sentiment.polarity
		subjectivity = message.sentiment.subjectivity

		Sentiments_list.append(sentiment)
		Subjectivity_list.append(subjectivity)
		tweet_text_list.append(raw_tweet_text)
		tweet_location_list.append(location)


	tweet_Data["sentiments"] = Sentiments_list
	tweet_Data["subjectivity"]= Subjectivity_list
	tweet_Data["location"] = tweet_location_list
	tweet_Data["text"] = tweet_text_list
	tweet_Data["coordinates"]=tweet_lat_lng_list

	

	#Let us calculate the sentiment scores

	return tweet_Data

def geocode_location(loc):
	#Importing the API key for Google Geocode
	gmaps_api = configurations.google_maps_key

	#Registering our app by sending the API key 
	gm = googlemaps.Client(key=gmaps_api)

	##################################################################
	#We need to geocode this location and store it as lat and longtitude
	location_result = gm.geocode(loc)
	if len(location_result) > 0:
		#means that atleast something was returned
		latitude = location_result[0]['geometry']['location']['lat']
		longitude= location_result[0]['geometry']['location']['lng']
		formatted = "["+str(latitude)+","+str(longitude)+"]"
		return formatted
		

	else:
		#store null
		return ""
	
	return
	##################################################################
