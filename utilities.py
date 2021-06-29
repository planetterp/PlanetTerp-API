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
    data = json.dumps({'error': message})
    return web.badrequest(data)

def get_limit(data, default, max_):
    limit = default

    if 'limit' in data:
        limit = data['limit']
        if not is_int(limit):
            raise api_error(f"limit parameter must be an integer between 1 and {max_}")
        limit = int(limit)
        if limit < 1 or limit > max_:
            raise api_error(f"limit parameter must be an integer between 1 and {max_}")
    return limit

def get_offset(data):
    offset = 0

    if 'offset' in data:
        offset = data['offset']
        if not is_int(offset):
            raise api_error("offset parameter must be an integer greater than or equal to 0")
        offset = int(offset)
        if offset < 0:
            raise api_error("offset parameter must be an integer greater than or equal to 0")
    return offset
