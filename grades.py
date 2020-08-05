import web
import model
import utilities
import json

class Grades:
	def GET(self):
		model.insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
		web.header('Content-Type', 'application/json')
		data = web.input()

		OPTIONS = []

		if not 'professor' in data and not 'course' in data:
			return utilities.api_error("parameters must include at least one of: \"course\", \"professor\"")

		if 'professor' in data:
			professor_id = model.get_professor_id(data['professor'])

			if not professor_id:
				return utilities.api_error("professor not found")

			OPTIONS.append("professor_id = {}".format(professor_id))

		if 'course' in data:
			course_id = model.get_course_id(data['course'])

			if not course_id:
				return utilities.api_error("course not found")

			OPTIONS.append("course_id = {}".format(course_id))

		if 'semester' in data:
			possible_semesters = ["201201", "201208", "201301", "201308", "201401", "201408", "201501", "201508", "201601", "201608", "201701", "201708", "201801", "201808", "201901", "201908"]

			if not data['semester'] in possible_semesters:
				return utilities.api_error("invalid semester parameter; semester parameter must be one of the following: " + ', '.join(possible_semesters))

			OPTIONS.append("semester = {}".format(data['semester']))

		if 'section' in data:
			all_sections = model.get_sections()

			# todo: more efficient way of doing this?
			if not any(section['section'] == data['section'] for section in all_sections):
				return utilities.api_error("invalid section; example of a valid section: 0101")

			OPTIONS.append("section = '{}'".format(data['section']))

		OPTIONS = ' AND '.join(OPTIONS)
		if OPTIONS:
			OPTIONS = ' WHERE ' + OPTIONS

		grades = model.get_grades(OPTIONS)
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