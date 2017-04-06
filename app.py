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

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    # print("Request:")
    # print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "movieTeller":
        return {}
    
    
    baseurl = "https://api.themoviedb.org/3/discover/movie?api_key=a6669e892c1628955e0af913f38dbb91"
    # result = urlopen(baseurl).read()
    # data = json.loads(result)
    # res = makeWebhookResult(data)

    params = checkParams(req)
    url = baseurl + params
    print ("URL")
    print (url)

    result = urlopen(url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)

    return res

def checkParams(req):
    result = req.get("result")
    parameters = result.get("parameters")
    keyword = parameters.get("keyword")

    print("KEYWORD: ")
    print(keyword)

    url_params = "&sort_by=popularity.desc"
    return url_params

def makeWebhookResult(data):
    # print ("WEBHOOOKRESULT: ")
    # print (data)

    total_results = data.get('total_results')
    # print("total_results") 
    # print (total_results)

    speech = "Total Number of Movies Found: " + str(total_results)

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
