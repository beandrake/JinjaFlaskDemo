from flask import Flask, render_template
from functools import wraps
import random
import datetime
import requests

DEBUG_MODE = True

app = Flask(__name__)


def callAPI(url, params={}):
	print(f"Calling {url} with params {str(params)}...")
	response = requests.get(url, params=params)
	response.raise_for_status()
	print(response)
	return response.json()


def applyHtmlTag(tag):
	def decorator(function):
		@wraps(function)
		def decoratedFunction(*args, **kwargs):
			result = function(*args, **kwargs)
			return f'<{tag}>{result}</{tag}>'
		return decoratedFunction
	return decorator


def renderTemplate(*args, **kwargs):
	'''A wrapper for render_template that provides an up-to-date year to put on the webpage.'''
	kwargs['currentYear'] = datetime.datetime.now().year
	return render_template(*args, **kwargs)

#########################################################################################################################

@app.route("/")
def home():
	'''Homepage that contains some general exploration of Flask and Jinja tech.'''
	numby = random.randint(1, 10)
	# The html file must be in the templates folder.
	# You can add as many kwargs as you want, so the html's Jinja can use them
	return renderTemplate('index.html', randomNumber=numby)


@app.route("/fizzbuzz")
def fizzbuzz():
	'''Uses the below API to list the most statistically likely age for the name in the URL.'''
	return renderTemplate('fizzbuzz.html')


@app.route(r"/guessAge/<name>")
def guessAge(name):
	'''Uses the below API to list the most statistically likely age for the name in the URL.'''
	api = f'https://api.agify.io?name={name}'
	result = callAPI(api)
	age = result.get('age')
	return renderTemplate('guessAge.html', name=name, age=age)


@app.route("/stringPage")
@applyHtmlTag('html')
@applyHtmlTag('body')
@applyHtmlTag('b')
@applyHtmlTag('u')
@applyHtmlTag('i')
def stringPage():
	return "If you wanted you could just make each webpage from a string!"


if __name__ == '__main__':
	app.run(debug=DEBUG_MODE)