import requests
import json
course_name = input("Enter a course: ")

grade_data = requests.get("https://api.planetterp.com/v1/grades?course=" + course_name).json()

if "error" in grade_data and grade_data['error'] == "course not found":
    print("Error: Course not found.")
else:
    for course_grade_data in grade_data:
            print("Number of students who received an A in {course} section {section} for semester {semester}: {num_a}".format(course = course_grade_data['course'], section = course_grade_data['section'], semester = course_grade_data['semester'], num_a = course_grade_data['A']))
