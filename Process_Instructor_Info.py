import json
import os

def calculate_instructor_details(directory):
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
            del course_dict['total_rating']

    # Save the details to a json file
    with open("instructor_details.json", 'w', encoding='utf-8') as outfile:
        json.dump(instructor_details, outfile, indent=4)

# Usage:
directory = './CourseInfo'
calculate_instructor_details(directory)
