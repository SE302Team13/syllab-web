import os
import ssl
import pandas as pd
ssl._create_default_https_context = ssl._create_unverified_context

lecture_name = "CE 221"

if not os.path.exists(lecture_name):
    os.makedirs(lecture_name)

df = pd.read_html(
    "https://ce.ieu.edu.tr/tr/syllabus/type/read/id/"+lecture_name.replace(" ", "+"))
for i, table in enumerate(df):
    print(0, table[0])
