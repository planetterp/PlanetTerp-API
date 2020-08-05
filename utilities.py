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
	limit = 100

	if 'limit' in data:
		limit = data['limit']
		if not is_int(limit):
			return api_error("limit parameter must be an integer between 1 and 1000")
		limit = int(limit)
		if limit < 1 or limit > 1000:
			return api_error("limit parameter must be an integer between 1 and 1000")
	return limit

def get_offset(data):
	offset = 0

	if 'offset' in data:
		offset = data['offset']
		if not is_int(offset):
			return api_error("offset parameter must be an integer greater than or equal to 0")
		offset = int(offset)
		if offset < 0:
			return api_error("offset parameter must be an integer greater than or equal to 0")
	return offset
