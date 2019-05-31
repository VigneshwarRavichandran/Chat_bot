from flask import Flask, jsonify, make_response, request
from response import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	return make_response(jsonify(results()))

def results():
	req = request.get_json(force=True)
	action = req['queryResult']['action']

	if action == 'get_response':
		response = get_response(req)
		return { "fulfillmentMessages" : response }
	
	elif action == 'get_date':
		response = get_date(req)
		return { "fulfillmentMessages" : response }

	elif action == 'get_timeslots':
		response = get_timeslots(req)
		return { "fulfillmentMessages" : response }
	
	elif action == 'get_time':
		response = get_time(req)
		return { "fulfillmentMessages" : response }

	elif action == 'get_email':
		response = get_email()
		return { "fulfillmentMessages" : response }

	elif action == 'get_event_positive_response':
		response = get_event_positive_response()
		return { "fulfillmentMessages" : response }

	elif action == 'get_event_note':
		response = get_event_note(req)
		return { "fulfillmentMessages" : response }

	elif action == 'get_event_negative_response':
		response = get_event_negative_response(req)
		return { "fulfillmentMessages" : response }
		
if __name__ == '__main__':
  app.run()
