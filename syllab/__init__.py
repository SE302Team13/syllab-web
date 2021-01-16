import logging
import requests
from bs4 import BeautifulSoup
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Syllab HTTP trigger function processed a request.')
    lang = req.params.get('lang')
    code = req.params.get('code').replace(" ", "+")
    logging.info(lang)
    logging.info(code)

    try:
        r = requests.get('http://ce.ieu.edu.tr/' + lang +
                         '/syllabus/type/read/id/' + code, verify=False)
    except requests.exceptions.ConnectionError:
        return func.HttpResponse(
            json.dumps({
                "message": "Connection Refused to IEU Server"
            }),
            mimetype="application/json"
        )

    source = BeautifulSoup(r.content, "html.parser")

    course_name = source.find(id='course_name').text.strip()
    course_code = code.replace("+", " ")
    course_semester = 0 if (source.find(id='semester').text.strip() == "Güz" or source.find(id='semester').text.strip() == "Fall") else (
        1 if (source.find(id='semester').text.strip() == "Bahar" or source.find(id='semester').text.strip() == "Spring") else 2)
    course_weekly_hours = source.find(id="weekly_hours").text.strip()
    course_application_hours = source.find(id="app_hours").text.strip()
    ieu_credit = source.find(id="ieu_credit").text.strip()
    ects_credit = source.find(id="ects_credit").text.strip()
    pre_req = source.find(id="pre_requisites").text.strip()
    course_lang = source.find(id="course_lang").text.strip()
    course_type = source.find(id="course_type").text.strip()
    level = source.find(id="course_level").text.strip()

    # yardımcılar
    yardimcilar = source.find(id="yardimci_list")
    assistants = []
    if(yardimcilar != None):
        for yardimci in yardimcilar:
            yardimci = {
                "link": yardimci.a['href'],
                "name": yardimci.text.strip()
            }
            assistants.append(yardimci)

    # hocalar
    lecturer_list = source.find(id="lecturer_list")
    lecturers = []
    if(lecturer_list != None):
        for lecturer in lecturer_list:
            lecturer = {
                "link": lecturer.a['href'],
                "name": lecturer.text.strip()
            }
            lecturers.append(lecturer)

    # koordinatör
    coordinator_list = source.find(id="coordinator_list")
    coordinators = []
    if(coordinator_list != None):
        for coordinator in coordinator_list:
            coordinator = {
                "link": coordinator.a['href'],
                "name": coordinator.text.strip()
            }
            coordinators.append(coordinator)

    # ders kategorileri
    core_course = source.find(id="core_course")
    major_area = source.find(id="major_area")
    supportive_courses = source.find(id="supportive_courses")
    media_man_skills = source.find(id="media_man_skills")
    trans_skills = source.find(id="trans_skills")

    categories = {
        "core_course": True if core_course.text.strip() == "X" else False,
        "major_area": True if major_area.text.strip() == "X" else False,
        "supportive_courses": True if supportive_courses.text.strip() == "X" else False,
        "media_man_skills": True if media_man_skills.text.strip() == "X" else False,
        "trans_skills": True if trans_skills.text.strip() == "X" else False
    }

    # haftalık konular
    weekly_subjects = []
    for i in range(16):
        hafta_str = "hafta_" + str(i+1)
        week = source.find(id=hafta_str).findAll('td')
        subject = {
            "subject": week[1].text.strip(),
            "reading": week[2].text.strip()
        }
        weekly_subjects.append(subject)

    # evaluation system
    attendance_no = source.find(id="attendance_no")
    attendance_per = source.find(id="attendance_per")

    lab_no = source.find(id="lab_no")
    lab_per = source.find(id="lab_per")

    fieldwork_no = source.find(id="fieldwork_no")
    fieldwork_per = source.find(id="fieldwork_per")

    quiz_no = source.find(id="quiz_no")
    quiz_per = source.find(id="quiz_per")

    homework_no = source.find(id="homework_no")
    homework_per = source.find(id="homework_per")

    presentation_no = source.find(id="presentation_no")
    presentation_per = source.find(id="presentation_per")

    project_no = source.find(id="project_no")
    project_per = source.find(id="project_per")

    seminar_no = source.find(id="seminar_no")
    seminar_per = source.find(id="seminar_per")

    portfolios_no = source.find(id="portfolios__no")
    portfolios_per = source.find(id="portfolios_per")

    midterm_no = source.find(id="midterm_no")
    midterm_per = source.find(id="midterm_per")

    final_no = source.find(id="final_no")
    final_per = source.find(id="final_per")

    evaluation = {
        "attendance": {
            "no": attendance_no.text.strip(),
            "per": attendance_per.text.strip()
        },
        "lab": {
            "no": lab_no.text.strip(),
            "per": lab_per.text.strip()
        },
        "fieldwork": {
            "no": fieldwork_no.text.strip(),
            "per": fieldwork_per.text.strip()
        },
        "quiz": {
            "no": quiz_no.text.strip(),
            "per": quiz_per.text.strip()
        },
        "homework": {
            "no": homework_no.text.strip(),
            "per": homework_per.text.strip()
        },
        "presentation": {
            "no": presentation_no.text.strip(),
            "per": presentation_per.text.strip()
        },
        "project": {
            "no": project_no.text.strip(),
            "per": project_per.text.strip()
        },
        "seminar": {
            "no": seminar_no.text.strip(),
            "per": seminar_per.text.strip()
        },
        "portfolios": {
            "no": portfolios_no.text.strip(),
            "per": portfolios_per.text.strip()
        },
        "midterm": {
            "no": midterm_no.text.strip(),
            "per": midterm_per.text.strip()
        },
        "final": {
            "no": final_no.text.strip(),
            "per": final_per.text.strip()
        }
    }

    # workload table
    course_hour_number = source.find(id="course_hour_number")
    course_hour_duration = source.find(id="course_hour_duration")
    course_hour_total_workload = source.find(id="course_hour_total_workload")

    lab_number = source.find(id="lab_number")
    lab_duration = source.find(id="lab_duration")
    lab_total_workload = source.find(id="lab_total_workload")

    out_hour_number = source.find(id="out_hour_number")
    out_hour_duration = source.find(id="out_hour_duration")
    out_hour_total_workload = source.find(id="out_hour_total_workload")

    fieldwork_number = source.find(id="fieldwork_number")
    fieldwork_duration = source.find(id="fieldwork_duration")
    fieldwork_total_number = source.find(id="fieldwork_total_number")

    quizess_number = source.find(id="quizess_number")
    quizess_duration = source.find(id="quizess_duration")
    quizess_total_workload = source.find(id="quizess_total_workload")

    homework_number = source.find(id="homework_number")
    homework_duration = source.find(id="homework_duration")
    homework_total_workload = source.find(id="homework_total_workload")

    presentation_number = source.find(id="presentation_number")
    presentation_duration = source.find(id="presentation_duration")
    presentation_total_workload = source.find(id="presentation_total_workload")

    project_number = source.find(id="project_number")
    project_duration = source.find(id="project_duration")
    project_total_workload = source.find(id="project_total_workload")

    seminar_number = source.find(id="seminar_number")
    seminar_duration = source.find(id="seminar_duration")
    seminar_total_workload = source.find(id="seminar_total_workload")

    portfolios_number = source.find(id="portfolios_number")
    portfolios_duration = source.find(id="portfolios_duration")
    portfolios_total_workload = source.find(id="portfolios_total_workload")

    midterm_number = source.find(id="midterm_number")
    midterm_duration = source.find(id="midterm_duration")
    midterm_total_workload = source.find(id="midterm_total_workload")

    final_number = source.find(id="final_number")
    final_duration = source.find(id="final_duration")
    final_total_workload = source.find(id="final_total_workload")

    workload = {
        "attendance": {
            "no": course_hour_number.text.strip(),
            "duration": course_hour_duration.text.strip(),
            "total_workload": course_hour_total_workload.text.strip()
        },
        "lab": {
            "no": lab_number.text.strip(),
            "duration": lab_duration.text.strip(),
            "total_workload": lab_total_workload.text.strip()
        },
        "out_hour": {
            "no": out_hour_number.text.strip(),
            "duration": out_hour_duration.text.strip(),
            "total_workload": out_hour_total_workload.text.strip()
        },
        "fieldwork": {
            "no": fieldwork_number.text.strip(),
            "duration": fieldwork_duration.text.strip(),
            "total_workload": fieldwork_total_number.text.strip()
        },
        "quiz": {
            "no": quizess_number.text.strip(),
            "duration": quizess_duration.text.strip(),
            "total_workload": quizess_total_workload.text.strip()
        },
        "homework": {
            "no": homework_number.text.strip(),
            "duration": homework_duration.text.strip(),
            "total_workload": homework_total_workload.text.strip()
        },
        "presentation": {
            "no": presentation_number.text.strip(),
            "duration": presentation_duration.text.strip(),
            "total_workload": presentation_total_workload.text.strip()
        },
        "project": {
            "no": project_number.text.strip(),
            "duration": project_duration.text.strip(),
            "total_workload": project_total_workload.text.strip()
        },
        "seminar": {
            "no": seminar_number.text.strip(),
            "duration": seminar_duration.text.strip(),
            "total_workload": seminar_total_workload.text.strip()
        },
        "oral_exam": {
            "no": portfolios_number.text.strip(),
            "duration": portfolios_duration.text.strip(),
            "total_workload": portfolios_total_workload.text.strip()
        },
        "midterm": {
            "no": midterm_number.text.strip(),
            "duration": midterm_duration.text.strip(),
            "total_workload": midterm_total_workload.text.strip()
        },
        "final": {
            "no": final_number.text.strip(),
            "duration": final_duration.text.strip(),
            "total_workload": final_total_workload.text.strip()
        }
    }

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
        "assistants": assistants,
        "coordinators": coordinators,
        "categories": categories,
        "weekly_subjects": weekly_subjects,
        "evaluation": evaluation,
        "workload_table": workload
    }

    return func.HttpResponse(
        json.dumps(course),
        mimetype="application/json"
    )
