import web
import model
import utilities
from utilities import JsonBadRequest
import json

class Search:
    def GET(self):
        model.insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status,
            web.ctx.ip, (web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT'
                in web.ctx.env else None), "GET")
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')

        data = web.input()

        if "query" not in data:
            raise JsonBadRequest("parameters must include \"query\"")

        query = data.query
        limit = utilities.get_limit(data, 30, 100)
        offset = utilities.get_offset(data)
        results = model.search(query, limit, offset)

        results_list = []
        for result in results:
            result = {
                "type": result.source,
                "name": result.name,
                "slug": result.slug,
            }
            results_list.append(result)

        return json.dumps(results_list)
