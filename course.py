import web
import model
import utilities

class Course:
	def GET(self):
		model.insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
		web.header('Content-Type', 'application/json')
		data = web.input()

		REVIEWS = False

		if not 'name' in data:
			return utilities.api_error("name parameter is required")

		if 'reviews' in data:
			if not data['reviews'] in TRUE_FALSE:
				return utilities.api_error("reviews parameter must be either true or false")

			if data['reviews'] == 'true':
				REVIEWS = True

		course = db.query('SELECT id, department, course_number, title, description, credits FROM courses WHERE CONCAT(department, course_number)=$name', vars={'name': data['name']})

		if len(course) == 0:
			return utilities.api_error("course not found")
		course = course[0]

		professors = model.get_professors_teaching_course(course['id'])
		course['professors'] = []
		for professor in professors:
			course['professors'].append(professor['name'])

		if REVIEWS:
			course['reviews'] = []
			reviews = model.get_reviews_course(course['id'])
			for review in reviews:
				course['reviews'].append({'professor': review['name'], 'course': course['department'] + course['course_number'], 'review': review['review'], 'rating': review['rating'], 'expected_grade': review['expected_grade'], 'created': review['review_created'].isoformat()})

		del course['id']

		return json.dumps(course)