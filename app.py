from flask import Flask, render_template
from tweets import QueryTwitter
import pandas as pd 
import json 

app = Flask(__name__)

@app.route("/")
def index():
	(a,b)=QueryTwitter("Python")
	#parse all the relevant information here and send to index.html
	#return tweetsDataframe.to_html()
	'''
	country = tweetsDataframe['country']
	latitude = tweetsDataframe['latitude']
	longitude = tweetsDataframe['longitude']
	language = tweetsDataframe['language']
	subjectivity_group = tweetsDataframe['subjectivity_group']
	sentiments_group = tweetsDataframe['sentiments_group']
	return render_template('index.html',country=country,latitude=latitude,longitude=longitude,language=language,subjectivity_group=subjectivity_group,sentiments_group=sentiments_group)
	'''
	return render_template('index.html',doughnut=json.dumps(a),sentiments_map=json.dumps(b))
	#return str(tweetsDataframe)

if __name__ == "__main__":
	app.run(debug=True, port=5000)