import requests
import csv
from pandas.io.json import json_normalize
import pandas as pd
import json
import flask
from flask_cors import CORS


app = flask.Flask()


@app.route('/git', method=['POST', 'GET'])
def get_data():
	


if __name__=='__main__':
	app.run()
