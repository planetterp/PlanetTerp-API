import web

db = web.database(dbn='mysql', db='planetterp', user='root', pw='', charset='utf8mb4')

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
