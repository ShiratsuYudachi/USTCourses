from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

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

def get_courseInfo_for(courseID):
    current_number_of_windows = len(driver.window_handles)
    driver.execute_script(f"window.open('https://ust.space/review/{courseID}', '_blank');")
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])  # 切换到新的窗口

