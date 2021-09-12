import web

db = web.database(dbn='mysql', db='planetterp', user='root', pw='', charset='utf8mb4')

def get_professors_teaching_course(course_id):
    return db.query('SELECT name FROM professor_courses INNER JOIN professors ON professor_courses.professor_id = professors.id WHERE professor_courses.course_id = $id AND professors.verified = TRUE', vars={'id': course_id}).list()

def get_courses_professor_teaches(professor_id):
    return db.query('SELECT CONCAT(department, course_number) AS course FROM professor_courses INNER JOIN courses ON professor_courses.course_id = courses.id WHERE professor_id = $id ORDER BY CONCAT(department, course_number) ASC', vars={'id': professor_id}).list()

def get_reviews(professor_id):
    professor_verified = db.query('SELECT * FROM professors WHERE id = $professor_id AND verified=TRUE', vars={'professor_id': professor_id})

    if len(professor_verified) != 1:
        return []

    return db.query('SELECT *, CONCAT(department, course_number) AS course, reviews.created AS review_created FROM reviews LEFT JOIN courses on reviews.course_id = courses.id WHERE professor_id = $id AND verified = TRUE', vars={'id': professor_id})

def get_reviews_course(course_id):
    return db.query('SELECT *, reviews.created AS review_created FROM reviews INNER JOIN professors ON reviews.professor_id = professors.id WHERE course_id = $course_id AND reviews.verified = TRUE AND professors.verified = TRUE', vars={'course_id': course_id})

def department_has_course(department):
    department = db.query('SELECT * FROM courses WHERE department = $department', vars={'department': department})

    if len(department) == 0:
        return False

    return True

def get_course(name, reviews):
    course = list(db.query('SELECT courses.id, department, course_number, title, description, credits, GROUP_CONCAT(name) AS professors FROM courses LEFT JOIN professor_courses ON professor_courses.course_id = courses.id LEFT JOIN professors ON professors.id = professor_courses.professor_id WHERE CONCAT(department, course_number) = $name GROUP BY courses.id', vars={'name': name}))

    if len(course) != 1:
        return None

    course = get_course_data(course[0], reviews)

    return course

def get_courses(limit, offset, department, reviews):
    if department:
        courses = list(db.query('SELECT courses.id, department, course_number, title, description, credits, GROUP_CONCAT(name) AS professors FROM courses LEFT JOIN professor_courses ON professor_courses.course_id = courses.id LEFT JOIN professors ON professors.id = professor_courses.professor_id WHERE department = $department GROUP BY courses.id ORDER BY CONCAT(department, course_number) LIMIT {} OFFSET {}'.format(limit, offset), vars={'department': department}))
    else:
        courses = list(db.query('SELECT courses.id, department, course_number, title, description, credits, GROUP_CONCAT(name) AS professors FROM courses LEFT JOIN professor_courses ON professor_courses.course_id = courses.id LEFT JOIN professors ON professors.id = professor_courses.professor_id GROUP BY courses.id ORDER BY CONCAT(department, course_number) LIMIT {} OFFSET {}'.format(limit, offset), vars={'department': department}))

    for course in courses:
        course = get_course_data(course, reviews)

    return courses

def get_course_data(course, reviews):
    if course['professors']:
        course['professors'] = course['professors'].split(',')
    else:
        course['professors'] = []

    course['average_gpa'] = get_average_gpa(course["id"])

    if reviews:
        course['reviews'] = []
        course_reviews = get_reviews_course(course['id'])
        for review in course_reviews:
            data = {
                'professor': review['name'],
                'course': course['department'] + course['course_number'],
                'review': review['review'],
                'rating': review['rating'],
                'expected_grade': review['expected_grade'],
                'created': review['review_created'].isoformat()
            }
            course['reviews'].append(data)

    del course['id']
    return course

# todo: find a better way to get professor and reviews
def get_professor(name, reviews):
    professor = list(db.query('SELECT professors.id AS id, name, slug, IF(type = 0, "professor", "ta") AS type, GROUP_CONCAT(CONCAT(department, course_number)) AS courses FROM professors LEFT JOIN professor_courses ON professor_courses.professor_id = professors.id LEFT JOIN courses ON courses.id = professor_courses.course_id WHERE professors.verified = TRUE AND name = $name GROUP BY professors.id', vars={'name': name}))

    if len(professor) != 1:
        return None

    professor = get_professor_data(professor[0], reviews)

    return professor

# todo: find a better way to get professors and reviews
def get_professors(limit, offset, type_, reviews):
    if type_:
        professors = list(db.query('SELECT professors.id AS id, name, slug, IF(type = 0, "professor", "ta") AS type, GROUP_CONCAT(CONCAT(department, course_number)) AS courses FROM professors LEFT JOIN professor_courses ON professor_courses.professor_id = professors.id LEFT JOIN courses ON courses.id = professor_courses.course_id WHERE professors.verified = TRUE AND type = $type GROUP BY professors.id ORDER BY name LIMIT {} OFFSET {}'.format(limit, offset), vars={'type': 0 if type_ == 'professor' else 1}))
    else:
        professors = list(db.query('SELECT professors.id AS id, name, slug, IF(type = 0, "professor", "ta") AS type, GROUP_CONCAT(CONCAT(department, course_number)) AS courses FROM professors LEFT JOIN professor_courses ON professor_courses.professor_id = professors.id LEFT JOIN courses ON courses.id = professor_courses.course_id WHERE professors.verified = TRUE GROUP BY professors.id ORDER BY name LIMIT {} OFFSET {}'.format(limit, offset)))

    for professor in professors:
        professor = get_professor_data(professor, reviews)

    return professors

def get_professor_data(professor, reviews):
    if professor['courses']:
        professor['courses'] = professor['courses'].split(',')
    else:
        professor['courses'] = []

    if reviews:
        professor['reviews'] = []
        professor_reviews = get_reviews(professor['id'])
        for review in professor_reviews:
            professor['reviews'].append({'professor': professor['name'], 'course': review['course'], 'review': review['review'], 'rating': review['rating'], 'expected_grade': review['expected_grade'], 'created': review['review_created'].isoformat()})

    average_rating = get_average_rating(professor['id'])

    if average_rating is not None:
        average_rating = float(average_rating)

    professor['average_rating'] = average_rating

    del professor['id']
    return professor

def get_professor_id(name):
    a = db.query('SELECT * FROM professors WHERE name = $name AND verified = TRUE', vars={'name': name})

    if len(a) == 0:
        return None

    return a[0]['id']

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

def get_sections():
    return db.query('SELECT section FROM grades')

def get_average_rating(professor_id):
    rating = db.query('SELECT SUM(rating)/COUNT(rating) AS average_rating FROM reviews WHERE professor_id = $id AND verified = TRUE', vars={'id': professor_id})

    if len(rating) != 1:
        return None

    return rating[0]['average_rating']

def get_average_gpa(course_id):
    average_gpa = db.query('SELECT (SUM(APLUS)*4.0 + SUM(A)*4.0 + SUM(AMINUS)*3.7 + SUM(BPLUS)*3.3 + SUM(B)*3.0 + SUM(BMINUS)*2.7 + SUM(CPLUS)*2.3 + SUM(C)*2.0 + SUM(CMINUS)*1.7 + SUM(DPLUS)*1.3 + SUM(D)*1.0 + SUM(DMINUS)*0.7 + SUM(F)*0.0 + SUM(W)*0.0 + SUM(OTHER)*0.0) / (SUM(num_students) - SUM(OTHER)) AS average_gpa FROM grades WHERE course_id = $course_id', vars={"course_id": course_id})[0]["average_gpa"]
    return float(average_gpa) if average_gpa else None

def get_semesters():
    semesters_list = db.query('SELECT DISTINCT semester FROM grades')

    return [semester['semester'] for semester in semesters_list]

def insert_view (page, status, ip, user_agent, method):
    db.insert('views', page = page, status = status, ip = ip, user_agent = user_agent, method = method)

def search(search, limit, offset):
    return db.query('SELECT name, slug, "professor" AS source FROM professors WHERE verified=true AND name LIKE $search UNION SELECT CONCAT(department, course_number) AS name, CONCAT(department, course_number) AS slug, "course" AS source FROM courses WHERE CONCAT(department, course_number) LIKE $search ORDER BY name ASC LIMIT $limit OFFSET $offset', vars={'search': '%{}%'.format(search), 'limit': limit, "offset": offset})
