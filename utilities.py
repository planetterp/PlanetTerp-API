import web
import json

TRUE_FALSE = ['true', 'false']

# modified from https://stackoverflow.com/q/354038
def is_int(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def api_error(message):
	web.ctx.status = "400 Bad Request"
	return json.dumps({'error': message})

def get_limit(data):
	LIMIT = 100

	if 'limit' in data:
		LIMIT = data['limit']
		if not is_int(LIMIT):
			return api_error("limit parameter must be an integer between 1 and 1000")
		LIMIT = int(LIMIT)
		if LIMIT < 1 or LIMIT > 1000:
			return api_error("limit parameter must be an integer between 1 and 1000")
	return LIMIT

def get_offset(data):
	OFFSET = 0

	if 'offset' in data:
		OFFSET = data['offset']
		if not is_int(OFFSET):
			return api_error("offset parameter must be an integer greater than or equal to 0")
		OFFSET = int(OFFSET)
		if OFFSET < 0:
			return api_error("offset parameter must be an integer greater than or equal to 0")
	return OFFSET
