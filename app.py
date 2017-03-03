from flask import Flask, render_template
from tweets import QueryTwitter
import pandas as pd 

app = Flask(__name__)

@app.route("/")
def index():
	tweetsDataframe=QueryTwitter("Python")

	return tweetsDataframe.to_html()
	#return tweetsDataframe
	#return "Hello World"


if __name__ == "__main__":
	app.run(debug=True, port=5000)