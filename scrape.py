from bs4 import BeautifulSoup
from re import *
from json import *

import course
import requests
    
r = requests.get("https://catalog.ucdavis.edu/courses-subject-code/sta/")
soup = BeautifulSoup(r.content, 'html.parser')
soup.find_all("div", class_="courseblock")

# scrapes courses and adds them to the courses dictionary in course.py
def scrapeCourses():
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
                    class_li = li
        
                label = li.find("span", class_="label")
                if label:
                    label_text = label.get_text(strip=True)
                    full_text = li.get_text(strip=True)

                    result = full_text.replace(label_text, "", 1).strip()

                    if "Course Description" in label_text:
                        courseDesc = result
                    elif "Prerequisite" in label_text:
                        coursePreReqs = result
            
            # Debugging
            # First, find the span with class "detail-code" within the li element
            # Gives something like STA 250 - Topics in Applied & Computational Statistics
            allCourses = class_li.find("span", class_="detail-code")
            
            # Now find only the first part, the course code
            courseCode = allCourses.find("a", class_="bubblelink code").text
            courseCode = "".join(courseCode.split())
            # print(courseCode)
        
            # Second part, get the name of the class
            h5 = allCourses.find("h5")
            children = list(h5.children)
            courseName = children[1].text
            courseName = courseName.replace("—", "").strip()
            
            # Split between units and course name
            splitString = courseName.split("(")

            # Course Name
            courseName = splitString[0].strip()

            # Course Units
            courseUnits = splitString[1].replace(")", "").strip()

            courseCode = courseCode.replace(" ", "")
            courseName = courseName.replace("—", "").strip()

        else:
            courseCode = block.find("span", class_="detail-code").text
            courseName = block.find("span", class_="detail-title").text
            courseUnits = block.find("span", class_="detail-hours_html").text
            coursePreReqsTag = block.find("p", class_="detail-prerequisite")
            coursePreReqs = coursePreReqsTag.get_text(" ", strip=True) if coursePreReqsTag else None
            
            courseCode = courseCode.replace(" ", "")
            courseName = courseName.replace("—", "").strip()
        
        courseObj = course.Course(courseName, courseCode, courseUnits, courseDesc, coursePreReqs)
        course.courses[courseCode] = courseObj

print(course.courses["STA108"].prerequisites)

