import requests
import csv
from pandas.io.json import json_normalize
import pandas as pd
import json
import flask
from flask_cors import CORS
from flask import request

app = flask.Flask(__name__)
CORS(app)


@app.route('/repos')
def get_repos():
	api = request.args.get("api-key")
	return api



@app.route('/branches')
def get_branches():
	repo_name = request.args.get('repo-name')
	owner_name = request.args.get('owner-name')
	api = request.args.get("api-key")

	pass

@app.route('/commit')
def get_commits():
	repo_name = request.args.get('repo-name')
	owner_name = request.args.get('owner-name')
	from_date = request.args.get('from-date')
	to_date = request.args.get('to-date')
	api = request.args.get("api-key")

	pass


if __name__=='__main__':
	app.run()
