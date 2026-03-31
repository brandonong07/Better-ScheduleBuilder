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
    courseDesc = block.find("p", class_="courseblockextra").text
    
    coursePreReqs = None
    header_li = None
    # Checking for outdated courses
    if "This version has ended;" in courseDesc:
        subBlock = block.find("div", class_="courseblockextra")
        lis = subBlock.find_all("li")
        header_li = None
        for li in lis:
            if li.find("span", class_="detail-code"):
                header_li = li
    
            label = li.find("span", class_="label")
            if label:
                label_text = label.get_text(strip=True)
                full_text = li.get_text(strip=True)

                result = full_text.replace(label_text, "", 1).strip()

                if "Course Description" in label_text:
                    courseDesc = result
                elif "Prerequisite" in label_text:
                    coursePreReqs = result
        print(header_li.find("span", class_="detail-code").text)
    else:
        courseCode = block.find("span", class_="detail-code").text
        courseName = block.find("span", class_="detail-title").text
        courseUnits = block.find("span", class_="detail-hours_html").text
        coursePreReqs = block.find("p", class_="detail-prerequisite")


    courseCode = courseCode.replace(" ", "")
    courseName = courseName.replace("—", "").strip()

    courseObj = course.Course(courseName, courseCode, courseUnits, courseDesc, coursePreReqs)
    course.courses[courseCode] = courseObj

