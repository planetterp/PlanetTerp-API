import web
import model
import utilities
from utilities import JsonBadRequest
import json

class Professor:
    def GET(self):
        model.insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')

        data = web.input()

        reviews = False

        if not 'name' in data:
            raise JsonBadRequest("name parameter is required")

        if 'reviews' in data:
            if not data['reviews'] in utilities.TRUE_FALSE:
                raise JsonBadRequest("reviews parameter must be either true or false")

            if data['reviews'] == 'true':
                reviews = True

        professor = model.get_professor(data['name'], reviews)

        if not professor:
            raise JsonBadRequest("professor not found")

        return json.dumps(professor)
