import web
import model
import utilities
import json

class Courses:
    def GET(self):
        model.insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')

        data = web.input()

        limit = utilities.get_limit(data)
        offset = utilities.get_offset(data)
        department = ""
        reviews = False

        if not utilities.is_int(limit):
            return limit
        if not utilities.is_int(offset):
            return offset

        if 'department' in data:
            if len(data['department']) != 4:
                return utilities.api_error("department parameter must be 4 characters")

            department = data['department']

            if not model.department_has_course(department):
                return utilities.api_error("no courses found with that department")

        if 'reviews' in data:
            if not data['reviews'] in utilities.TRUE_FALSE:
                return utilities.api_error("reviews parameter must be either true or false")

            if data['reviews'] == 'true':
                reviews = True

        courses = model.get_courses(limit, offset, department, reviews)

        return json.dumps(list(courses))
