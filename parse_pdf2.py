import camelot

file = "https://ects.ieu.edu.tr/new/PDF_syllabus.php?section=ce.cs.ieu.edu.tr&course_code=CE+215&cer=&sem=&lang=en"

tables = camelot.read_pdf(file, pages="1-end")


# first table
course_code = tables[0].df[0][1]
semester = tables[0].df[1][1]
theoric_hours = tables[0].df[2][1]
app_hours = tables[0].df[3][1]
ieu_credit = tables[0].df[4][1]
ects = tables[0].df[5][1]

# Second Table
prereq = tables[1].df[1][0]
lang = tables[1].df[1][1]
crs_type = tables[1].df[1][2]
level = tables[1].df[1][3]
coordinator = tables[1].df[1][4].split("\n")
lecturers = tables[1].df[1][5].split("\n")
assistants = tables[1].df[1][6].split("\n")

course = {
    "code": course_code,
    "semester": semester,
    "weekly_hours": theoric_hours,
    "app_hours": app_hours,
    "ieu_credit": ieu_credit,
    "ects_credit": ects,
    "pre_req": prereq,
    "language": lang,
    "type": crs_type,
    "level": level,
    "coordinators": coordinator,
    "lecturers": lecturers,
    "assistants": assistants
}

print(course)
