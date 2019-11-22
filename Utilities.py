import json
import pandas as pd
import requests


def check_daterange(date):
    """
    first arg is from date
    second arg is to date
    """
    from_date = date[0]
    to_date = date[1]
    if from_date < to_date:
        return [True, None]
    else:
        return [False, None]


# get all the commits of the users for that branch
def getCommitBasedAuthor(authors, dateRange, api, owner, repo):
    checker = check_daterange(dateRange)
    #     print(dateRange)
    if checker[0]:
        url = "https://api.github.com/repos/" + owner + "/" + repo + "/commits"

        collaborators = authors
        newCollab = []
        collab_data = []
        df = pd.DataFrame()
        headers = {
            'Authorization': "Bearer " + api,
            'User-Agent': "PostmanRuntime/7.15.0",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Postman-Token': "b77a6841-03c5-4bd9-8859-32b338b5d64b,a0ef9990-1be3-4ea3-b295-5efd2e97c2f3",
            'Host': "api.github.com",
            'accept-encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }

        for i in collaborators:
            x = 0
            while True:
                # fecthing only one page, so there is no incrementing of x
                querystring = {"sha": "Development", "per_page": "100", "page": x + 1, "author": i,
                               "since": str(dateRange[0]) + "Z",
                               "until": str(dateRange[1]) + "Z"}
                response = requests.request("GET", url, headers=headers, params=querystring)
                data = json.loads(response.text)
                df_c = pd.io.json.json_normalize(data)
                x = x + 1
                if not df_c.empty:
                    newCollab.append(i)
                    collab_data.append({i: df_c.copy()})
                else:
                    break

        return collab_data, newCollab, True

    else:
        return checker[0], checker[1], False


# function to get all the author for the repo and branch
def getAllCollaborators(owner, repo, api):
    auths = []
    url = "https://api.github.com/repos/"+ owner + "/" + repo +"/collaborators"

    querystring = {"owner": owner, "repo": repo}

    headers = {
        'Authorization': "Bearer " + api ,
        'User-Agent': "PostmanRuntime/7.15.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "44816ac8-8b9c-4c62-8c60-e68675737d20,4503cdd6-27d5-4618-8313-76e0ac20a3a8",
        'Host': "api.github.com",
        'accept-encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    authsResponse = json.loads(response.text)
    for x in authsResponse:
        auths.append((x['login']))

    return auths


def mergeAllData(names, data):
    i = 0
    listing = pd.DataFrame()
    for x in names:
        listing = listing.append(data[i][x])
        i +=1
    return listing

def collaborate(data, names):
    allData = mergeAllData(names, data)
    tableFormat = allData.groupby(['commit.author.date','author.login']).count()['author.id'].reset_index(name='count')
    tableFormat['commit.author.date'] = pd.to_datetime(tableFormat['commit.author.date']).dt.date
    tableFormat = tableFormat.groupby(['commit.author.date','author.login']).sum()['count'].reset_index(name='count')
    return pd.DataFrame(tableFormat)