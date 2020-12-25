import requests
from bs4 import BeautifulSoup

r = requests.get('https://ce.ieu.edu.tr/tr/syllabus/type/read/id/CE+350')
source = BeautifulSoup(r.content,"html.parser")


course_name = source.find(id='course_name').text.strip()
course_code = source.find(id='course_code')
course_semester = 0 if source.find(id='semester').text.strip() == "Güz"  else ( 1 if source.find(id='semester').text.strip() == "Bahar" else 2) 
course_weekly_hours = int(source.find(id="weekly_hours").text.strip())

course = {
    "name": course_name,
    "code": course_code,
    "semester": course_semester,
    "weekly_hours": course_weekly_hours
}

print(course)




