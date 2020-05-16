#!/usr/bin/env python
# from livereload import Server

import web
import json

urls = (
	'/', 'Index',
	'/v1', 'VersionOne',
	'/v1/course', 'Course',
	'/v1/courses', 'Courses',
	'/v1/professor', 'Professor',
	'/v1/professors', 'Professors',
	'/v1/grades', 'Grades'
)

web.config.debug = True
app = web.application(urls, globals())
db = web.database(dbn='mysql', db='planetterp', user='root', pw='', charset='utf8mb4')
render = web.template.render('templates', globals={'str': str})

TRUE_FALSE = ['true', 'false']

def get_professors_teaching_course(course_id):
	return db.query('SELECT name FROM professor_courses INNER JOIN professors ON professor_courses.professor_id = professors.id WHERE professor_courses.course_id = $id AND professors.verified=1', vars={'id': course_id}).list()

def get_courses_professor_teaches(professor_id):
	return db.query('SELECT CONCAT(department, course_number) AS course FROM professor_courses INNER JOIN courses ON professor_courses.course_id = courses.id WHERE professor_id = $id ORDER BY CONCAT(department, course_number) ASC', vars={'id': professor_id}).list()

def get_reviews(professor_id):
	return db.query('SELECT *, CONCAT(department, course_number) AS course, reviews.created AS review_created FROM reviews LEFT JOIN courses on reviews.course_id = courses.id WHERE professor_id = $id AND verified = true ORDER BY reviews.created DESC', vars={'id': professor_id})

def get_reviews_course(course_id):
	return db.query('SELECT *, reviews.created AS review_created FROM reviews LEFT JOIN professors ON reviews.professor_id = professors.id WHERE course_id = $course_id AND reviews.verified = true AND professors.verified = true ORDER BY reviews.created DESC', vars={'course_id': course_id})

def get_professor_id(name):
	a = db.query('SELECT * FROM professors WHERE name=$name', vars={'name': name})

	if len(a) == 0:
		return None

	return a[0]['id']

def get_professor_from_id(id_):
	try:
		return db.select('professors', where = 'id = $id', vars={'id': id_})[0]
	except IndexError:
		return None

def get_course_id(course_name):
	department = course_name[:4]
	course_number = course_name[4:]

	course = db.select('courses', where='department = $department AND course_number = $course_number', vars={'department': department, 'course_number': course_number})

	if len(course) == 1:
		return course[0]['id']

	return None

def get_course_from_id(id_):
	try:
		return db.select('courses', where = 'id = $id', vars={'id': id_})[0]
	except IndexError:
		return None

def get_grades(options):
	grades_data = db.query('SELECT department, course_number, name, semester, section, APLUS, A, AMINUS, BPLUS, B, BMINUS, CPLUS, C, CMINUS, DPLUS, D, DMINUS, F, W, OTHER FROM grades LEFT JOIN courses ON courses.id = grades.course_id LEFT JOIN professors ON professors.id = grades.professor_id {} ORDER BY semester DESC'.format(options))
	return grades_data

def insert_view (page, status, ip, user_agent, method):
	db.insert('views', page = page, status = status, ip = ip, user_agent = user_agent, method = method)

# modified from https://stackoverflow.com/q/354038
def is_int(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def api_error(message):
	web.ctx.status = "400 Bad Request"
	return json.dumps({'error': message})

def get_limit(data):
	LIMIT = 100

	if 'limit' in data:
		LIMIT = data['limit']
		if not is_int(LIMIT):
			return api_error("limit parameter must be an integer between 1 and 1000")
		LIMIT = int(LIMIT)
		if LIMIT < 1 or LIMIT > 1000:
			return api_error("limit parameter must be an integer between 1 and 1000")
	return LIMIT

def get_offset(data):
	OFFSET = 0

	if 'offset' in data:
		OFFSET = data['offset']
		if not is_int(OFFSET):
			return api_error("offset parameter must be an integer greater than or equal to 0")
		OFFSET = int(OFFSET)
		if OFFSET < 0:
			return api_error("offset parameter must be an integer greater than or equal to 0")
	return OFFSET


class Index:
	def GET(self):
		insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
		return render.index()


class VersionOne:
	def GET(self):
		insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
		web.header('Content-Type', 'application/json')
		return json.dumps({'version': 1, 'documentation': 'https://api.planetterp.com'})


class Course:
	def GET(self):
		insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
		web.header('Content-Type', 'application/json')
		data = web.input()

		REVIEWS = False

		if not 'name' in data:
			return api_error("name parameter is required")

		if 'reviews' in data:
			if not data['reviews'] in TRUE_FALSE:
				return api_error("reviews parameter must be either true or false")

			if data['reviews'] == 'true':
				REVIEWS = True

		course = db.query('SELECT id, department, course_number, title, description, credits FROM courses WHERE CONCAT(department, course_number)=$name', vars={'name': data['name']})

		if len(course) == 0:
			return api_error("course not found")
		course = course[0]

		professors = get_professors_teaching_course(course['id'])
		course['professors'] = []
		for professor in professors:
			course['professors'].append(professor['name'])

		if REVIEWS:
			course['reviews'] = []
			reviews = get_reviews_course(course['id'])
			for review in reviews:
				course['reviews'].append({'professor': review['name'], 'course': course['department'] + course['course_number'], 'review': review['review'], 'rating': review['rating'], 'expected_grade': review['expected_grade'], 'created': review['review_created'].isoformat()})

		del course['id']

		return json.dumps(course)


class Courses:
	def GET(self):
		insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
		web.header('Content-Type', 'application/json')
		data = web.input()

		LIMIT = get_limit(data)
		OFFSET = get_offset(data)
		DEPARTMENT = ""
		REVIEWS = False

		if not is_int(LIMIT):
			return LIMIT
		if not is_int(OFFSET):
			return OFFSET

		if 'department' in data:
			if len(data['department']) != 4:
				return api_error("department parameter must be 4 characters")

			DEPARTMENT = data['department']

		if 'reviews' in data:
			if not data['reviews'] in TRUE_FALSE:
				return api_error("reviews parameter must be either true or false")

			if data['reviews'] == 'true':
				REVIEWS = True

		if DEPARTMENT == "":
			courses = db.query('SELECT id, department, course_number, title, description, credits FROM courses ORDER BY CONCAT(department, course_number) LIMIT {} OFFSET {}'.format(LIMIT, OFFSET), vars={'department': DEPARTMENT})
		else:
			courses = db.query('SELECT id, department, course_number, title, description, credits FROM courses WHERE department=$department ORDER BY CONCAT(department, course_number) LIMIT {} OFFSET {}'.format(LIMIT, OFFSET), vars={'department': DEPARTMENT})

		courses = list(courses)
		for course in courses:
			professors = get_professors_teaching_course(course['id'])
			course['professors'] = []
			for professor in professors:
				course['professors'].append(professor['name'])

			if REVIEWS:
				course['reviews'] = []
				reviews = get_reviews_course(course['id'])
				for review in reviews:
					course['reviews'].append({'professor': review['name'], 'course': course['department'] + course['course_number'], 'review': review['review'], 'rating': review['rating'], 'expected_grade': review['expected_grade'], 'created': review['review_created'].isoformat()})

			del course['id']

		return json.dumps(list(courses))


class Professor:
	def GET(self):
		insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
		web.header('Content-Type', 'application/json')
		data = web.input()

		REVIEWS = False

		if 'reviews' in data:
			if not data['reviews'] in TRUE_FALSE:
				return api_error("reviews parameter must be either true or false")

			if data['reviews'] == 'true':
				REVIEWS = True

		if not 'name' in data:
			return api_error("name parameter is required")

		professor = db.query('SELECT id, name, slug, IF(type=0, "professor", "ta") AS type FROM professors WHERE verified=1 AND name = $name', vars={'name': data['name']})
		if len(professor) == 0:
			return api_error("professor not found")
		professor = professor[0]
		courses = get_courses_professor_teaches(professor['id'])
		professor['courses'] = []
		for course in courses:
			professor['courses'].append(course['course'])

		if REVIEWS:
			professor['reviews'] = []
			reviews = get_reviews(professor['id'])
			for review in reviews:
				print review['review']
				professor['reviews'].append({'professor': professor['name'], 'course': review['course'], 'review': review['review'].encode('utf-8'), 'rating': review['rating'], 'expected_grade': review['expected_grade'], 'created': review['review_created'].isoformat()})

		del professor['id']

		return json.dumps(professor)


class Professors:
	def GET(self):
		insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
		web.header('Content-Type', 'application/json')
		data = web.input()

		LIMIT = get_limit(data)
		OFFSET = get_offset(data)
		TYPE = ""
		REVIEWS = False

		if not is_int(LIMIT):
			return LIMIT
		if not is_int(OFFSET):
			return OFFSET

		PROFESSOR_TYPES = ['professor', 'ta']
		if 'type' in data:
			if not data['type'] in PROFESSOR_TYPES:
				return api_error("type parameter must be either \"professor\" or \"ta\"")

			TYPE = data['type']

		if 'reviews' in data:
			if not data['reviews'] in TRUE_FALSE:
				return api_error("reviews parameter must be either true or false")

			if data['reviews'] == 'true':
				REVIEWS = True

		if TYPE == "":
			professors = db.query('SELECT id, name, slug, IF(type=0, "professor", "ta") AS type FROM professors WHERE verified=1 ORDER BY name LIMIT {} OFFSET {}'.format(LIMIT, OFFSET))
		else:
			professors = db.query('SELECT id, name, slug, IF(type=0, "professor", "ta") AS type FROM professors WHERE verified=1 AND type=$type ORDER BY name LIMIT {} OFFSET {}'.format(LIMIT, OFFSET), vars={'type': 0 if TYPE == 'professor' else 1})
		professors = list(professors)
		for professor in professors:
			courses = get_courses_professor_teaches(professor['id'])
			professor['courses'] = []
			for course in courses:
				professor['courses'].append(course['course'])

			if REVIEWS:
				professor['reviews'] = []
				reviews = get_reviews(professor['id'])
				for review in reviews:
					print review['review']
					professor['reviews'].append({'professor': professor['name'], 'course': review['course'], 'review': review['review'].encode('utf-8'), 'rating': review['rating'], 'expected_grade': review['expected_grade'], 'created': review['review_created'].isoformat()})

			del professor['id']

		return json.dumps(list(professors))


class Grades:
	def GET(self):
		insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
		web.header('Content-Type', 'application/json')
		data = web.input()

		OPTIONS = []

		if not 'professor' in data and not 'course' in data:
			return api_error("parameters must include at least one of: \"course\", \"professor\"")

		if 'professor' in data:
			professor_id = get_professor_id(data['professor'])

			if not professor_id:
				return api_error("professor not found")

			OPTIONS.append("professor_id = {}".format(professor_id))

		if 'course' in data:
			course_id = get_course_id(data['course'])

			if not course_id:
				return api_error("course not found")

			OPTIONS.append("course_id = {}".format(course_id))

		if 'semester' in data:
			possible_semesters = ["201201", "201208", "201301", "201308", "201401", "201408", "201501", "201508", "201601", "201608", "201701", "201708", "201801", "201808", "201901", "201908"]

			if not data['semester'] in possible_semesters:
				return api_error("invalid semester parameter; semester parameter must be one of the following: " + ', '.join(possible_semesters))

			OPTIONS.append("semester = {}".format(data['semester']))

		OPTIONS = ' AND '.join(OPTIONS)
		if OPTIONS:
			OPTIONS = ' WHERE ' + OPTIONS

		grades = get_grades(OPTIONS)
		grades_data = []

		for course_grade in grades:
			if course_grade['department'] and course_grade['course_number']:
				course = course_grade['department'] + course_grade['course_number']
			else:
				course = None
			grades_data.append({
				'course': course,
				'professor': course_grade['name'],
				'semester': course_grade['semester'],
				'section': course_grade['section'],
				'A+': course_grade['APLUS'],
				'A': course_grade['A'],
				'A-': course_grade['AMINUS'],
				'B+': course_grade['BPLUS'],
				'B': course_grade['B'],
				'B-': course_grade['BMINUS'],
				'C+': course_grade['CPLUS'],
				'C': course_grade['C'],
				'C-': course_grade['CMINUS'],
				'D+': course_grade['DPLUS'],
				'D': course_grade['D'],
				'D-': course_grade['DMINUS'],
				'F': course_grade['F'],
				'W': course_grade['W'],
				'Other': course_grade['OTHER']
			})

		return json.dumps(grades_data)
	

if __name__ == "__main__":
	app.run()


