import requests
from bs4 import BeautifulSoup

r = requests.get('https://ce.ieu.edu.tr/en/syllabus/type/read/id/CE+350')
source = BeautifulSoup(r.content, "html.parser")


course_name = source.find(id='course_name').text.strip()
course_code = source.find(id='course_code')
# needs sooo better solution, for example languages are still a problem
course_semester = 0 if source.find(id='semester').text.strip() == "Güz" else (
    1 if source.find(id='semester').text.strip() == "Bahar" else 2)
course_weekly_hours = int(source.find(id="weekly_hours").text.strip())
course_application_hours = int(source.find(id="app_hours").text.strip())
ieu_credit = int(source.find(id="ieu_credit").text.strip())
ects_credit = int(source.find(id="ects_credit").text.strip())
pre_req = source.find(id="pre_requisites").text.strip()
course_lang = source.find(id="course_lang").text.strip()
course_type = source.find(id="course_type").text.strip()
level = source.find(id="course_level").text.strip()

# yardımcılar
yardimcilar = source.find(id="yardimci_list")
assistants = []
for yardimci in yardimcilar:
    yardimci = {
        "link": yardimci.a['href'],
        "name": yardimci.text.strip()
    }
    assistants.append(yardimci)

# yardımcılar
lecturer_list = source.find(id="lecturer_list")
lecturers = []
for lecturer in lecturer_list:
    lecturer = {
        "link": lecturer.a['href'],
        "name": lecturer.text.strip()
    }
    lecturers.append(lecturer)

course = {
    "name": course_name,
    "code": course_code,
    "semester": course_semester,
    "weekly_hours": course_weekly_hours,
    "app_hours": course_application_hours,
    "ieu_credit": ieu_credit,
    "ects_credit": ects_credit,
    "pre_req": pre_req,
    "course_lang": course_lang,
    "course_type": course_type,
    "level": level,
    "lecturers": lecturers,
    "assistants": assistants

}

print(course)
