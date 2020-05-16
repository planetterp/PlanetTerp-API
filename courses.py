import web
import model
import utilities

class Courses:
	def GET(self):
		model.insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
		web.header('Content-Type', 'application/json')
		data = web.input()

		LIMIT = utiltiies.get_limit(data)
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

		if 'reviews' in data:
			if not data['reviews'] in TRUE_FALSE:
				return utilities.api_error("reviews parameter must be either true or false")

			if data['reviews'] == 'true':
				REVIEWS = True

		if DEPARTMENT == "":
			courses = db.query('SELECT id, department, course_number, title, description, credits FROM courses ORDER BY CONCAT(department, course_number) LIMIT {} OFFSET {}'.format(LIMIT, OFFSET), vars={'department': DEPARTMENT})
		else:
			courses = db.query('SELECT id, department, course_number, title, description, credits FROM courses WHERE department=$department ORDER BY CONCAT(department, course_number) LIMIT {} OFFSET {}'.format(LIMIT, OFFSET), vars={'department': DEPARTMENT})

		courses = list(courses)
		for course in courses:
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

		return json.dumps(list(courses))