from flask import Flask, render_template
from tweets import QueryTwitter

import tweepy
import numpy as np
import configurations 
import pandas as pd


app = Flask(__name__)

@app.route("/")
def index():
	#return "<h1>Hello World</h1>"
	#return render_template('index.html')
	tweets_fetched=QueryTwitter("Python")
	return str(tweets_fetched)
	#return "Hello World"





if __name__ == "__main__":
	app.run(debug=True, port=5000)