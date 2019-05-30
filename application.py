#!/usr/bin/env python3

import boto3
import api_keys

from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)
dynamo = boto3.resource('dynamodb')

gps = dynamo.Table('gps-data')

@app.route("/")
def index():
	response = gps.query(KeyConditionExpression=Key('deviceid').eq('gps-data/xps-9560'))

	entries = []
	for e in (p['payload'] for p in response['Items']):
		lat_deg = e['latitude'][0:2]
		lat_min = e['latitude'][2:-1]
		lat_dir = e['latitude'][-1]

		lng_deg = e['longitude'][0:3]
		lng_min = e['longitude'][3:-1]
		lng_dir = e['longitude'][-1]

		e['datetime'] = datetime.fromtimestamp(e['datetime']).ctime()

		e['latitude']  = '{}\u00b0 {}\' {}'.format(lat_deg, lat_min, lat_dir)
		e['lat_deg']   = (float(lat_deg) + float(lat_min) / 60) * (1 if lat_dir == 'N' else -1)

		e['longitude'] = '{}\u00b0 {}\' {}'.format(lng_deg, lng_min, lng_dir)
		e['lng_deg']   = (float(lng_deg) + float(lng_min) / 60) * (1 if lng_dir == 'E' else -1)

		e['altitude']  = '{:.2f}'.format(float(e['altitude'][0:-1]))

		e['speed'] = '{:.2f}'.format(float(e['speed']))
		e['direction'] = '{}\u00b0'.format(e['direction'])

		entries.append(e)

	entries.reverse()
	return render_template('index.html', entries=entries, maps_key=api_keys.google_maps_key)

if __name__ == '__main__':
	app.debug = True
	app.run()
