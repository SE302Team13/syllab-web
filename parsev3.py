import requests
import json
import re
from bs4 import BeautifulSoup
r = requests.get(
    'https://ects.ieu.edu.tr/new/PDF_syllabus.php?section=ce.cs.ieu.edu.tr&course_code=SE+116&cer=&sem=&lang=en')

source = BeautifulSoup(r.text, "html.parser")


print(source)
