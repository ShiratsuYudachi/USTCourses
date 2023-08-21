import requests
import json
import os

def cookie_string_to_dict(cookie_string):
    cookie_dict = {}
    for item in cookie_string.split('; '): 
        if '=' in item:
            key, value = item.split('=', 1)
            cookie_dict[key] = value
    return cookie_dict

cookie_str = "_ga=GA1.2.1370733350.1660261914; remember_82e5d2c56bdd0811318f0cf078b78bfc=eyJpdiI6IkNlS3VEU28rSW8yZitjUGR5bCtjRWc9PSIsInZhbHVlIjoiU3JYTkhackNvbWtSeEtvUXp6OWRyRDRKb3VXUExEWjNiS2M1KzNicWh6ZUlMRGxyMVBld3IwZkdndE00Tm56VCt3MTdGSGVUcWNCY0tzQ29VaGozN0JCRm5CdUplY3RVXC9Edmc5dFlTTXJnPSIsIm1hYyI6IjFhMDA3NjhkNWE5MjVmMzk1NDQxM2U0OTIxMzMyNDhmZDQ2YWEwY2EwMmY5YmY1OWY1ZTVjNzljMmZlNzU0YWQifQ%3D%3D; _gid=GA1.2.1189473322.1692645874; XSRF-TOKEN=eyJpdiI6Imp3ZEJpczBkMGc2djVvcmtSUnZUMXc9PSIsInZhbHVlIjoicFNrVjNWV0N4OHBCYUVxell6YUFzeERjYmM4ZFMwTWttMEd1c2ZaaXJ3TVplWkVRT1I1THFTYXRDMDk5NkJ4VEdLT1dTNkJNTXlrUFN3WTJcL3NOSHpBPT0iLCJtYWMiOiIxMzhmMTIzYTJkNWQ1OGVhNjA0YTMxNjYxOGE3ZWQ1ZGRhOTk0NGI0OTRmYjBhYWM5Y2I5YjdiM2ZiZGI4MTU1In0%3D; ustspace_session=eyJpdiI6IjRhYkhcL0FUUU9cLzF5YXhiS2MrUGJZQT09IiwidmFsdWUiOiJTOTBha0VLRVBuajhvektXTXVGT0lNZDNsMXNmWnBaVEFlQlMydGJ1TVlzcG1TYXNmT21lRVdsZjAzR3VZREJPNTZvRkpsY01EYXlLYVNzQlhVUm9Cdz09IiwibWFjIjoiYWU2N2ZjNmM0NGExZGNjMDljMzM0MmMzYThiZTgzNDcyYmM3OTZiNzVhODM5ZmFiOWY2MzMwMWEwYzQ4ZTM2NSJ9; _gali=main-selector-list; _gat=1; _ga_MVRBNC746G=GS1.2.1692645874.10.1.1692646235.60.0.0"
cookies = cookie_string_to_dict(cookie_str)

def fetch_course_reviews(course_code):
    url = f"https://ust.space/review/{course_code}/get?single=false&composer=false&preferences%5Bsort%5D=0&preferences%5BfilterInstructor%5D=0&preferences%5BfilterSemester%5D=0&preferences%5BfilterRating%5D=0"

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-csrf-token": "PSwLwmUstmgQafkVWarqOfQBbNE8IZb9I2bM1M9H",
        "x-requested-with": "XMLHttpRequest"
    }

    response = requests.get(url, headers=headers, cookies=cookies)
    return response.json()

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))

def read_course_codes(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]
   

if not os.path.exists('./CourseInfo'):
    os.mkdir('./CourseInfo')

course_codes = read_course_codes('./courselist.txt')
total_courses = len(course_codes)

for index, course in enumerate(course_codes):
    target_filename = f'./CourseInfo/{course}.json'
    
    # Check if the file already exists
    if not os.path.exists(target_filename):
        reviews = fetch_course_reviews(course)
        save_to_json(reviews, target_filename)
    
    # Print the current progress
    print(f'Processing {index+1}/{total_courses} : {course}')

print("All courses processed!")