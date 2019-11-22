import json

from Utilities import getCommitBasedAuthor, getAllCollaborators
import flask
from flask_cors import CORS
from flask import request, Response

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
	authorNames = getAllCollaborators(owner_name, repo_name, api)
	data, names, status = getCommitBasedAuthor(authorNames, [from_date, to_date], api,
											   owner_name, repo_name)

	if status:
		return Response(response=json.dumps(data))
	else:
		return Response(status=401)



if __name__=='__main__':
	app.run()
