
from pathlib import Path
import requests
import tabula
filename = Path('metadata.pdf')
url = 'https://ects.ieu.edu.tr/new/PDF_syllabus.php?section=ce.cs.ieu.edu.tr&course_code=CE+215&cer=&sem=&lang=en'
response = requests.get(url)
filename.write_bytes(response.content)

tables = tabula.read_pdf("metadata.pdf", pages=1, multiple_tables=True)

# First Table
course_name = tables[0]["Code"][1]
semester = tables[0]["Semester"][1]
theoric_hours = tables[0]["Theory"][1]
app_hours = tables[0]["Application/Laboratory"][1]
ieu_credit = tables[0]["Local"][1]
ects = tables[0]["ECTS"][1]
#print(course_name, semester, theoric_hours, app_hours, ieu_credit, ects)

# Second Table
print(tables[1].pivot_table(index=['Prerequisites', 'None'], dtype=str))
prerequisites = tables[1].columns.values[1]
course_language = tables[1][tables[1].columns.values[1]][0]
course_type = tables[1][tables[1].columns.values[1]][1]

# print(tables[1][tables[1].columns.values[1]][1])

# third table
