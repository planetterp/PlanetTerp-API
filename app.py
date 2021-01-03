#!/usr/bin/env python
# from livereload import Server

import web
import json
import model
import course
import courses
import professor
import professors
import grades

urls = (
	'/', 'Index',
	'/v1', 'VersionOne',
	'/v1/course', course.Course,
	'/v1/courses', courses.Courses,
	'/v1/professor', professor.Professor,
	'/v1/professors', professors.Professors,
	'/v1/grades', grades.Grades
)

web.config.debug = False
app = web.application(urls, globals())
render = web.template.render('templates', globals={'str': str})

class Index:
	def GET(self):
		model.insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
		return render.index()


class VersionOne:
	def GET(self):
		model.insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
		web.header('Content-Type', 'application/json')
		web.header('Access-Control-Allow-Origin', '*')
		return json.dumps({'version': 1, 'documentation': 'https://api.planetterp.com'})


if __name__ == "__main__":
	app.run()


