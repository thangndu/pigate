import os
from flask import Flask, request
import redis
import requests
import json


app = Flask(__name__)


r = redis.Redis(host='xxxxx', port='xxxx', password='xxxxx')


@app.route('/')
def dashboard():

    plate_number = r.hget('pigate','plate_number')
    access_time = r.hget('pigate','access_time')
    access_status = r.hget('pigate','access_status')

    headers = request.headers.get('X-Forwarded-For', request.remote_addr)

    header = headers.split(",")
    access_ipaddress = header[0]

    url = "http://ip-api.com/json/" + access_ipaddress

    response = requests.get(url)
    data = json.loads(response.content)

    if data['status'] == "success":
    	access_location = data['city'] + ", " + data['country']
    else:
        access_location = "None"

    
    begin_html = """
    <html lang="en">
    <head>
  	<title>Pi Gate Dashboard</title>
  	<meta charset="utf-8">
  	<meta name="viewport" content="width=device-width, initial-scale=1">
    	<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
	<meta http-equiv="Pragma" content="no-cache" />
	<meta http-equiv="Expires" content="0" />
  	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    </head>
    <body>
    """

    end_html = "</body></html>"

    mid_html = """
    <div class="container-fluid">
  	<h1>
  	    <p class="text-center">Pi Gate Dashboard</p>
  	</h1>
        <div class="row">
    	    <div class="col-sm-12">
    	    	<img class="center-block" src="https://platenumber.s3.amazonaws.com/platenumber.jpg">
    	    </div>
  	</div>
  	<div class="row">
    	    <div class="col-sm-6" style="background-color:lavender;">
    		<p class="text-right">Plate number</p>
    	    </div>
    	    <div class="col-sm-6" style="background-color:lavenderblush;">
    	    	<p class="text-left">{}</p>
    	    </div>
  	</div>
  	<div class="row">
    	    <div class="col-sm-6" style="background-color:LightCyan;">
    		<p class="text-right">Access time</p>
    	    </div>
    	    <div class="col-sm-6" style="background-color:Bisque;">
    	    	<p class="text-left">{}</p>
    	    </div>
  	</div>
	<div class="row">
    	    <div class="col-sm-6" style="background-color:Pink;">
    		<p class="text-right">Access location</p>
    	    </div>
    	    <div class="col-sm-6" style="background-color:Orange;">
    	    	<p class="text-left">{}</p>
    	    </div>
  	</div>
  	<div class="row">
    	    <div class="col-sm-6" style="background-color:Khaki;">
    		<p class="text-right">Access status</p>
    	    </div>
    	    <div class="col-sm-6" style="background-color:PaleTurquoise;">
    		<p class="text-left">{}</p>
    	    </div>
  	</div>
    </div>
    """.format(plate_number,access_time,access_location,access_status)
    
    return begin_html + mid_html + end_html

if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
