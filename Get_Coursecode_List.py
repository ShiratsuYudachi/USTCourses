from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import requests
import re

#Chrome should be launched with debugger enabled
chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application"
#command: ./chrome.exe --remote-debugging-port=9223 --user-data-dir="D:\tempFolder"

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
driver = webdriver.Chrome(options=chrome_options)
print(driver.current_url)
print(driver.title) 


#delete old version when update is wanted, else it will simply write extra lines to old version
def get_courseID_list(): 
    ul_element = driver.find_elements(By.CLASS_NAME,'half')
    for department_i in range(len(ul_element)):
        department = driver.find_elements(By.CLASS_NAME,'half')[department_i]
        try:
            department.click()
        except Exception:
            continue
        
        WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,'li[data-type="course-review"]'))
        )

        courses = driver.find_elements(By.CSS_SELECTOR,'li[data-type="course-review"]')
        for i in courses:
            courseID = i.get_attribute('data-value')
            print(courseID)
            with open("courselist.txt",'a') as f:
                f.write(courseID+'\n')

        previous = driver.find_element(By.CLASS_NAME,'previous')
        previous.click()
        WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME,'half'))
        )

def Legacy_get_courseInfo_for(courseID):
    courseInfo = {}

    current_number_of_windows = len(driver.window_handles)
    driver.execute_script(f"window.open('https://ust.space/review/{courseID}', '_blank');")
    WebDriverWait(driver, 3).until(EC.number_of_windows_to_be(current_number_of_windows+1))
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME,'course-review-record'))
        )
    
    reviews = driver.find_elements(By.CLASS_NAME,'course-review-record')
    reviews_list = []
    for review in reviews:
        review_dict = {}
        review_dict['hash'] = review.get_attribute('data-hash')
        review_dict['title'] = review.find_element(By.CLASS_NAME,'course-review-record-title').text
        review_dict['semester'] = review.find_element(By.CLASS_NAME,'semester').text

        instructors = []
        instructors_isGood = []
        for i in review.find_element(By.CLASS_NAME,'details').find_elements(By.TAG_NAME,"em"):
            instructors.append(i.text)
            instructors_isGood.append(len(i.find_elements(By.CLASS_NAME,"fa-thumbs-up"))>=1) # can find thumbs up emoji
        
        review_dict['instructors'] = instructors
        review_dict['instructors_isGood'] = instructors_isGood

        review_dict['rating'] = [x.text for x in review.find_element(By.CLASS_NAME,'rating-container').find_elements(By.CLASS_NAME, 'rating')]
        comments = [x.get_attribute('innerHTML') for x in review.find_element(By.CLASS_NAME,'readmore-content').find_elements(By.CLASS_NAME, 'column')]
        for i in range(len(comments)):
            comments[i] = re.findall(r'<p>(.*?)<\/p>', comments[i])[0].replace('<br>','\n')
        review_dict['comments'] = comments

        print(review_dict)
        reviews_list.append(review_dict)
    courseInfo["reviews"] = reviews_list


def read_course_codes(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]
