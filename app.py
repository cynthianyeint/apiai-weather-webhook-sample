#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

import nltk
import requests

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request: ")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    # if req.get("result").get("action") != "movieTeller":
    #     return {}
    
    
    baseurl = "https://api.themoviedb.org/3/discover/movie?api_key=a6669e892c1628955e0af913f38dbb91&"
    params = checkParams(req)
    url = baseurl + params
    
    result = urlopen(url).read()
    data = json.loads(result)
    res = makeWebhookResult(req, data)

    return res

def checkParams(req):
    result = req.get("result")
    parameters = result.get("parameters")
    keyword = parameters.get("keyword")

    # context = result.get("contexts")[0]
    # context_name = context.get("name")

    # print("PARAMETERS: ")
    # print (parameters)

    # print ("CONTEXT: ")
    # print (context)

    # print ("CONTEXT NAME: ")
    # print(context_name)

    # print("KEYWORD: ")
    # print(keyword)

    if keyword == "popular":
        url_params  = "sort_by=popularity.desc"
    elif keyword == "cinemas":
        url_params = "primary_release_date.gte=2014-09-15&primary_release_date.lte=2014-10-22"
    elif keyword == "kid":
        url_params = "certification_country=US&certification.lte=G&sort_by=popularity.desc"
    else:
        url_params = "&sort_by=popularity.desc"
    return url_params

def makeWebhookResult(req, data):
    
    total_results = data.get('total_results')
    
    if req.get("result").get("action") == "movieTeller":
        speech = req.get("result").get("action") + "(two-way-new)We found " + str(total_results) + " movies."
    elif req.get("result").get("action") == "sentimentTeller":
        senti_text = {'text':'boring'}
        senti_data = requests.post("http://text-processing.com/api/sentiment/", 
                                    body=senti_text, )
        print("senti_data: ")
        print (senti_data)
        speech = "Testing Sentiment " + req.get("result").get("resolvedQuery")
    else:
        speech = "Wrong Action"

    # speech = req.get("result").get("action") + "(two-way-new)We found " + str(total_results) + " movies."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
