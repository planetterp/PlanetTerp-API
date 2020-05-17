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

def get_course(name):
	course = db.query('SELECT id, department, course_number, title, description, credits FROM courses WHERE CONCAT(department, course_number)=$name', vars={'name': name})

	if len(course) !=1:
		return None

	return course[0]

def get_courses(limit, offset, department):
	if department:
		courses = db.query('SELECT id, department, course_number, title, description, credits FROM courses WHERE department=$department ORDER BY CONCAT(department, course_number) LIMIT {} OFFSET {}'.format(limit, offset), vars={'department': department})
	else:
		courses = db.query('SELECT id, department, course_number, title, description, credits FROM courses ORDER BY CONCAT(department, course_number) LIMIT {} OFFSET {}'.format(limit, offset))

	return courses

def get_professor(name):
	professor = db.query('SELECT id, name, slug, IF(type=0, "professor", "ta") AS type FROM professors WHERE verified=1 AND name = $name', vars={'name': name})

	if len(professor) !=1 :
		return None

	return professor[0]

# todo: find a better way to get professors and reviews
def get_professors(limit, offset, type_, reviews):
	# if type_:
	professors = list(db.query('SELECT professors.id AS professor_id, name, slug, IF(type = 0, "professor", "ta") AS type, GROUP_CONCAT(CONCAT(department, course_number)) AS courses, (SELECT CONCAT(courses.department, courses.course_number) FROM courses WHERE reviews.course_id = courses.id ) AS course_review, review, rating, expected_grade, reviews.created AS created FROM professors INNER JOIN professor_courses ON professor_courses.professor_id = professors.id INNER JOIN courses ON courses.id = professor_courses.course_id INNER JOIN reviews ON reviews.professor_id = professors.id WHERE professors.verified = 1 AND reviews.verified=1 GROUP BY professors.id, reviews.id ORDER BY name LIMIT {} OFFSET {}'.format(limit, offset)))
	# else:
		# professors = db.query('SELECT id, name, slug, IF(type=0, "professor", "ta") AS type FROM professors WHERE verified=1 AND type = $type ORDER BY name LIMIT {} OFFSET {}'.format(limit, offset), vars={'type': type_})
	professors_data = []
	for professor in professors:
		cur_professor = None
		for temp_professor in professors_data:
			if professor['name'] == temp_professor['name']:
				cur_professor = temp_professor
				break

		if not cur_professor:
			professors_data.append({'name': professor['name'],
									'type': professor['type'],
									'slug': professor['slug'],
									'courses': professor['courses'].split(','),
									'reviews': []})
			cur_professor = professors_data[-1]

		cur_professor['reviews'].append({'professor': professor['name'],
										 'course': professor['course_review'],
										 'review': professor['review'],
										 'rating': professor['rating'],
										 'expected_grade': professor['expected_grade'],
										 'created': professor['created'].isoformat()})
	return professors_data

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

def get_professor_courses(professor_id):
	courses = get_courses_professor_teaches(professor_id)
	return [course['course'] for course in courses]

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
