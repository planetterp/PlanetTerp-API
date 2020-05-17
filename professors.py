import web
import model
import utilities
import json

class Professors:
	def GET(self):
		model.insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
		web.header('Content-Type', 'application/json')
		data = web.input()

		LIMIT = utilities.get_limit(data)
		OFFSET = utilities.get_offset(data)
		TYPE = ""
		REVIEWS = False

		if not utilities.is_int(LIMIT):
			return LIMIT
		if not utilities.is_int(OFFSET):
			return OFFSET

		PROFESSOR_TYPES = ['professor', 'ta']
		if 'type' in data:
			if not data['type'] in PROFESSOR_TYPES:
				return utilities.api_error("type parameter must be either \"professor\" or \"ta\"")

			TYPE = data['type']

		if 'reviews' in data:
			if not data['reviews'] in utilities.TRUE_FALSE:
				return utilities.api_error("reviews parameter must be either true or false")

			if data['reviews'] == 'true':
				REVIEWS = True

		professors = list(model.get_professors(LIMIT, OFFSET, TYPE, REVIEWS))
		# for professor in professors:
		# 	professor['courses'] = model.get_professor_courses(professor['id'])

		# 	if REVIEWS:
		# 		professor['reviews'] = []
		# 		reviews = model.get_reviews(professor['id'])
		# 		for review in reviews:
		# 			print review['review']
		# 			professor['reviews'].append({'professor': professor['name'], 'course': review['course'], 'review': review['review'].encode('utf-8'), 'rating': review['rating'], 'expected_grade': review['expected_grade'], 'created': review['review_created'].isoformat()})

		# 	del professor['id']

		return json.dumps(list(professors))