import web
import model
import utilities
import json

class Professors:
    def GET(self):
        model.insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
        web.header('Content-type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')

        data = web.input()

        limit = utilities.get_limit(data)
        offset = utilities.get_offset(data)
        type_ = ""
        reviews = False

        if not utilities.is_int(limit):
            return limit
        if not utilities.is_int(offset):
            return offset

        PROFESSOR_TYPES = ['professor', 'ta']
        if 'type' in data:
            if not data['type'] in PROFESSOR_TYPES:
                return utilities.api_error("type parameter must be either \"professor\" or \"ta\"")

            type_ = data['type']

        if 'reviews' in data:
            if not data['reviews'] in utilities.TRUE_FALSE:
                return utilities.api_error("reviews parameter must be either true or false")

            if data['reviews'] == 'true':
                reviews = True

        professors = list(model.get_professors(limit, offset, type_, reviews))

        return json.dumps(list(professors))
