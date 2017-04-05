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

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest1(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = makeYqlQuery(req)
    if yql_query is None:
        return {}
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res

def processRequest(req):
    rest = req.get("result")
    action = rest.get("action")
    parameters = rest.get("parameters")
    city = parameters.get("geo-city")

    if action !="yahooWeatherForecast":
        return {}
    baseurl = "https://api.themoviedb.org/3/discover/movie?api_key=a6669e892c1628955e0af913f38dbb91&sort_by=popularity.desc"
    result = urlopen(baseurl).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res

def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    print ("WEBHOOOKRESULT: ")
    print (data)

    total_results = data.get('total_results')
    print("total_results") 
    print (total_results)

    # result = data.get('results')
    # print ("RESULT: ")
    # print (result)

    rs = "Num: " + str(305417)
    print("res:")
    print(rs)
    
    # speech = "Today in " + data.get('total_results') + ": " + condition.get('text') + \
    #          ", the temperature is " + condition.get('temp') + " " + units.get('temperature')
    speech = "Total Number of Movies Found: "

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
