import json
from web import HTTPError

TRUE_FALSE = ['true', 'false']

# modified from https://stackoverflow.com/q/354038
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

class JsonBadRequest(HTTPError):
    message = "bad request"

    def __init__(self, message):
        status = "400 Bad Request"
        headers = {"Content-Type": "text/json"}
        message = json.dumps({'error': message})
        HTTPError.__init__(self, status, headers, message)

def get_limit(data, default, max_):
    limit = default

    if 'limit' in data:
        limit = data['limit']
        if not is_int(limit):
            raise JsonBadRequest(f"limit parameter must be an integer between 1 and {max_}")
        limit = int(limit)
        if limit < 1 or limit > max_:
            raise JsonBadRequest(f"limit parameter must be an integer between 1 and {max_}")
    return limit

def get_offset(data):
    offset = 0

    if 'offset' in data:
        offset = data['offset']
        if not is_int(offset):
            raise JsonBadRequest("offset parameter must be an integer greater than or equal to 0")
        offset = int(offset)
        if offset < 0:
            raise JsonBadRequest("offset parameter must be an integer greater than or equal to 0")
    return offset
