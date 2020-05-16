import web
import model
import utilities

class Professor:
	def GET(self):
		model.insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
		web.header('Content-Type', 'application/json')
		data = web.input()

		REVIEWS = False

		if 'reviews' in data:
			if not data['reviews'] in TRUE_FALSE:
				return utilities.api_error("reviews parameter must be either true or false")

			if data['reviews'] == 'true':
				REVIEWS = True

		if not 'name' in data:
			return utilities.api_error("name parameter is required")

		professor = db.query('SELECT id, name, slug, IF(type=0, "professor", "ta") AS type FROM professors WHERE verified=1 AND name = $name', vars={'name': data['name']})
		if len(professor) == 0:
			return utilities.api_error("professor not found")
		professor = professor[0]
		courses = model.get_courses_professor_teaches(professor['id'])
		professor['courses'] = []
		for course in courses:
			professor['courses'].append(course['course'])

		if REVIEWS:
			professor['reviews'] = []
			reviews = model.get_reviews(professor['id'])
			for review in reviews:
				print review['review']
				professor['reviews'].append({'professor': professor['name'], 'course': review['course'], 'review': review['review'].encode('utf-8'), 'rating': review['rating'], 'expected_grade': review['expected_grade'], 'created': review['review_created'].isoformat()})

		del professor['id']

		return json.dumps(professor)