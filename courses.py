import web
import model
import utilities
import json

class Courses:
	def GET(self):
		model.insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
		web.header('Content-Type', 'application/json')
		data = web.input()

		LIMIT = utilities.get_limit(data)
		OFFSET = utilities.get_offset(data)
		DEPARTMENT = ""
		REVIEWS = False

		if not utilities.is_int(LIMIT):
			return LIMIT
		if not utilities.is_int(OFFSET):
			return OFFSET

		if 'department' in data:
			if len(data['department']) != 4:
				return utilities.api_error("department parameter must be 4 characters")

			DEPARTMENT = data['department']

			if not model.department_has_course(DEPARTMENT):
				return utilities.api_error("no courses found with that department")

		if 'reviews' in data:
			if not data['reviews'] in utilities.TRUE_FALSE:
				return utilities.api_error("reviews parameter must be either true or false")

			if data['reviews'] == 'true':
				REVIEWS = True

		courses = model.get_courses(LIMIT, OFFSET, DEPARTMENT, REVIEWS)

		return json.dumps(list(courses))

