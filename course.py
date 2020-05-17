import web
import model
import utilities
import json

class Course:
	def GET(self):
		model.insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
		web.header('Content-Type', 'application/json')
		data = web.input()

		REVIEWS = False

		if not 'name' in data:
			return utilities.api_error("name parameter is required")

		if 'reviews' in data:
			if not data['reviews'] in utilities.TRUE_FALSE:
				return utilities.api_error("reviews parameter must be either true or false")

			if data['reviews'] == 'true':
				REVIEWS = True

		course = model.get_course(data['name'], REVIEWS)

		if not course:
			return utilities.api_error("course not found")

		return json.dumps(course)

