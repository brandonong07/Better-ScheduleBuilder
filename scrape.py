from bs4 import BeautifulSoup
import json
import re
import course
import requests


def clean_prereq_text(text):
    if not text:
        return None

    text = text.replace("\xa0", " ")
    text = text.replace("Prerequisite(s):", "").strip()

    # Separate course code from grade requirement
    text = re.sub(
        r'([A-Z]{2,5}\s*\d+[A-Z]*)([A-F][+-]?)\s*-\s*or better',
        r'\1 \2- or better',
        text
    )

    # Fix glued connectors like orSTA / andMAT
    text = re.sub(r'(or|and)([A-Z]{2,5}\s*\d)', r'\1 \2', text)
    text = re.sub(r'([A-Z]{2,5}\s*\d+[A-Z]*)(or|and)', r'\1 \2', text)

    # Add missing space after semicolon/comma when glued
    text = re.sub(r';(?=\S)', '; ', text)
    text = re.sub(r',(?=\S)', ', ', text)

    # Add missing space before advisory words when glued to course codes
    text = re.sub(r'([A-Z]{2,5}\s*\d+[A-Z]*)(strongly recommended)', r'\1 \2', text)
    text = re.sub(r'([A-Z]{2,5}\s*\d+[A-Z]*)(recommended)', r'\1 \2', text)
    text = re.sub(r'([A-Z]{2,5}\s*\d+[A-Z]*)(desirable)', r'\1 \2', text)
    text = re.sub(r'([A-Z]{2,5}\s*\d+[A-Z]*)(preferred)', r'\1 \2', text)

    # Normalize "Consent of instructor. Graduate standing." style cases
    text = re.sub(r'Consent of instructor\.\s*Graduate standing\.', 
                  'Consent of instructor; graduate standing.', text)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Remove extra spaces before punctuation
    text = re.sub(r'\s+([,.;])', r'\1', text)

    # Normalize spaces just inside parentheses
    text = re.sub(r'\(\s+', '(', text)
    text = re.sub(r'\s+\)', ')', text)

    # Normalize None
    if text.lower() == "none":
        return "None"

    return text

def get_course_links(session):
    base = "https://catalog.ucdavis.edu"
    website = base + "/courses-subject-code/"
    r = session.get(website, timeout=10)
    soup = BeautifulSoup(r.content, 'html.parser')

    course_links = []

    for link in soup.find_all('a', href=True):
        href = link['href']

        if href.startswith("/courses-subject-code/") and href != "/courses-subject-code/" and not href.endswith(".pdf"):
            full_link = base + href
            course_links.append(full_link)

    return list(dict.fromkeys(course_links))

# scrapes courses and adds them to the courses dictionary in course.py
def scrapeCourses(session, website=None):
    if website is None:
        website = "https://catalog.ucdavis.edu/courses-subject-code/sta/"
    r = requests.get(website, timeout=10)
    soup = BeautifulSoup(r.content, 'html.parser')

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
                        coursePreReqs = clean_prereq_text(result)
            
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
            coursePreReqs = clean_prereq_text(coursePreReqsTag.get_text(" ", strip=True)) if coursePreReqsTag else None
            
            courseCode = courseCode.replace(" ", "")
            courseName = courseName.replace("—", "").strip()
        
        courseObj = course.Course(courseName, courseCode, courseUnits, courseDesc, coursePreReqs)
        course.courses[courseCode] = courseObj

session = requests.Session()
websiteList = get_course_links(session)

for website in websiteList:
    print("Scraping:" + website)
    scrapeCourses(session, website)

# export here
data = {code: course.to_dict() for code, course in course.courses.items()}

with open("courses.json", "w") as f:
    json.dump(data, f, indent=2)
