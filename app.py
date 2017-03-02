from flask import Flask, render_template
from tweets import QueryTwitter

app = Flask(__name__)

@app.route("/")
def index():
	tweets_fetched=QueryTwitter("Python")
	return str(tweets_fetched)
	#return "Hello World"


if __name__ == "__main__":
	app.run(debug=True, port=5000)