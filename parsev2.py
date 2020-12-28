import requests
import json
import re
from bs4 import BeautifulSoup
r = requests.get('https://ce.ieu.edu.tr/en/syllabus/type/read/id/SE+115')

source = BeautifulSoup(r.content, "html.parser")

tables = source.findAll("table")

print(BeautifulSoup(str(tables[4]), "html.parser").findAll(
    "td")[5].text.strip())
