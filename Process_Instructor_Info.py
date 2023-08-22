import json
import os

directory = './CourseInfo'

def bayesian_rating(positive_reviews, total_reviews, C=0.7, M=10):
    return (C * M + positive_reviews) / (M + total_reviews)

def calculate_instructor_details(directory = directory):
    instructor_details = {}  # A dict to store cumulative ratings, counts, and course details

    # Iterate through all JSON files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                    course = data.get('course', {})
                    course_name = course.get('name', 'Unknown Course')
                    course_code = course.get('subject', 'Unknown Subject') + course.get('code', 'Unknown Code')
                    
                    for review in data.get('reviews', []):
                        for instructor in review.get('instructors', []):
                            name = instructor['name']
                            rating = instructor['rating']
                            
                            # If instructor not in dict, initialize their details
                            if name not in instructor_details:
                                instructor_details[name] = {
                                    'total_rating': 0,
                                    'count': 0,
                                    'courses': []
                                }
                            
                            instructor_details[name]['total_rating'] += rating
                            instructor_details[name]['count'] += 1
                            
                            # Track course details
                            course_exist = False
                            for course_dict in instructor_details[name]['courses']:
                                if course_dict['name'] == course_name:
                                    course_dict['count'] += 1
                                    course_dict['total_rating'] += rating
                                    course_exist = True
                                    break
                            
                            if not course_exist:
                                instructor_details[name]['courses'].append({
                                    'code': course_code,
                                    'name': course_name,
                                    'count': 1,
                                    'total_rating': rating
                                })

                except Exception as e:
                    print(f"Error processing {filename}. Error: {e}")

    # Calculate average ratings for overall and for each course
    for instructor, details in instructor_details.items():
        details['average_rating'] = details['total_rating'] / details['count']
        
        for course_dict in details['courses']:
            course_dict['avg_rating'] = course_dict['total_rating'] / course_dict['count']

        details['bayes_rating'] = bayesian_rating(details['total_rating'],details['count'])

    # Save the details to a json file
    with open("assets/instructor_details.json", 'w', encoding='utf-8') as outfile:
        json.dump(instructor_details, outfile, indent=4)

#The following is useable but have problem.
import openai
from api_key import *
def get_incontext_instructors(context):
    openai.api_type = api_type
    openai.api_base = api_base
    openai.api_version = api_version
    openai.api_key = api_key
    instruction = "Instruction: You are simulating an python function, which takes a string, a university course review, it maybe in English, Chinese or Cantonese as input and output instructor name mentioned the review. if it specified who is the instructor (saying 'instructor is a PhD student' or 'instructor is a Professor'is not specifying instructor), output the instructor FULL name only. Else, output None. DO NOT include any title like 'Dr.' or 'Prof.' or prefix like 'output: Amir' Your output should be like 'None', 'Amir' or 'Zilan Yang', and should NOT like 'Zilan Yang (Ph.D. student in accounting)', 'PhD candidate', 'Professor', 'Prof Chan'. Your output will directly be used in program so do not contain any explaination， do not include my input in your answer. \nInput:"
    response = openai.ChatCompletion.create(
        engine="gpt-35-turbo",
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": context}
        ]
    )
    return(response['choices'][0]['message']['content'].replace('instructor: ','').replace('Instructor: ','').strip('.').replace('Professor','').strip(' '))

def count_empty_instructors():
    dir_name = "CourseInfo"
    files = os.listdir(dir_name)

    total_reviews = 0
    empty_instructors_count = 0

    for file_name in files:
        with open(os.path.join(dir_name, file_name), 'r', encoding='utf-8') as infile:
            data = json.load(infile)
            reviews = data.get('reviews', [])

            for review in reviews:
                total_reviews += 1
                instructors = review.get('instructors', [])
                if not instructors:
                    empty_instructors_count += 1

    print(f"Total reviews: {total_reviews}")
    print(f"Reviews with empty instructors: {empty_instructors_count}")

from time import sleep
def extract_instructors_from_context(specified_coursecode = None):
    api_results = {}
    dir_name = "CourseInfo"
    files = os.listdir(dir_name)
    total_files = len(files)
    if os.path.exists('assets/missing_instructor_results.json'):
        with open('assets/missing_instructor_results.json', 'r', encoding='utf-8') as infile:
            api_results = json.load(infile)


    for index, file_name in enumerate(files, 1):
        with open(os.path.join(dir_name, file_name), 'r', encoding='utf-8') as infile:
            data = json.load(infile)
            if (specified_coursecode):
                try:
                    if not data['course']['subject']+data['course']['code'] in specified_coursecode:
                        continue
                except:
                    print("ERROR finding course! filename= "+file_name)
            reviews = data.get('reviews', [])
            for review in reviews:
                if review['hash'] in api_results:
                    continue
                instructors = review.get('instructors', [])
                if not instructors:
                    # Construct the context string from all comments
                    context = ""
                    for comment_key in ['comment_content', 'comment_teaching', 'comment_workload', 'comment_grading']:
                        context += review.get(comment_key, "")
                    hash = review['hash']
                    instructorName = ''
                    err_count = 0
                    while err_count<3:
                        try:
                            instructorName = get_incontext_instructors(context)
                            print(f"got response: {instructorName} \tat {file_name}, hash=\t{hash}")
                            break
                        except Exception:
                            print(f"!!!ERROR!!!: at {file_name}, hash={hash}, retrying in 1s")
                            sleep(1)
                            err_count+=1

                    api_results[hash] = instructorName
                    with open('assets/missing_instructor_results.json', 'w', encoding='utf-8') as outfile:
                        json.dump(api_results, outfile, ensure_ascii=False, indent=4)
        print(f"Processed {index}/{total_files} files")
    print("Finished processing all files.")

#extract_instructors_from_context()

