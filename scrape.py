from bs4 import BeautifulSoup
from re import *
from json import *

import course
import requests
    
r = requests.get("https://catalog.ucdavis.edu/courses-subject-code/sta/")
soup = BeautifulSoup(r.content, 'html.parser')
soup.find_all("div", class_="courseblock")


# def __init__(self, name, code, units, description):
blocks = soup.find_all("div", class_="courseblock")
for block in blocks:
    courseCode = block.find("span", class_="detail-code").text
    courseName = block.find("span", class_="detail-title").text
    courseUnits = block.find("span", class_="detail-hours_html").text
    courseDesc = block.find("p", class_="courseblockextra").text

    courseCode = courseCode.replace(" ", "")
    courseName = courseName.replace("—", "").strip()

    courseObj = course.Course(courseName, courseCode, courseUnits, courseDesc)
    course.courses[courseCode] = courseObj
