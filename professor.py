import web
import model
import utilities
import json

class Professor:
	def GET(self):
		model.insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
		web.header('Content-Type', 'application/json')
		data = web.input()

		REVIEWS = False

		if 'reviews' in data:
			if not data['reviews'] in utilities.TRUE_FALSE:
				return utilities.api_error("reviews parameter must be either true or false")

			if data['reviews'] == 'true':
				REVIEWS = True

		if not 'name' in data:
			return utilities.api_error("name parameter is required")

		professor = model.get_professor(data['name'])
		
		if not professor:
			return utilities.api_error("professor not found")

		professor['courses'] = model.get_professor_courses(professor['id'])

		if REVIEWS:
			professor['reviews'] = []
			reviews = model.get_reviews(professor['id'])
			for review in reviews:
				professor['reviews'].append({'professor': professor['name'], 'course': review['course'], 'review': review['review'].encode('utf-8'), 'rating': review['rating'], 'expected_grade': review['expected_grade'], 'created': review['review_created'].isoformat()})

		del professor['id']

		return json.dumps(professor)