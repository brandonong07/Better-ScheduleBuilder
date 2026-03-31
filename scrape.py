from bs4 import BeautifulSoup
from re import *
from json import *

import course
import requests
    
r = requests.get("https://catalog.ucdavis.edu/courses-subject-code/sta/")
soup = BeautifulSoup(r.content, 'html.parser')
soup.find_all("div", class_="courseblock")


sta10code = soup.find_all("span", class_="detail-code")[0].text
sta10title = soup.find_all("span", class_="detail-title")[0].text
sta10units = soup.find_all("span", class_="detail-hours_html")[0].text

print(sta10units)