import json
import Process_Instructor_Info

def display_subject_professors_ratings(subject):
    # Load the details from the json file
    with open("assets/instructor_details.json", 'r', encoding='utf-8') as infile:
        instructor_details = json.load(infile)

    subject_professors = []

    for instructor, details in instructor_details.items():
        relevant_courses = [course for course in details['courses'] if course['code'].startswith(subject)]
        if relevant_courses:
            subject_professors.append({
                'name': instructor,
                'average_rating': details['average_rating'],
                'count': details['count'],
                'courses': relevant_courses
            })

    # Sort professors by average rating in descending order
    subject_professors.sort(key=lambda x: x['bayes_rating'], reverse=True)

    # Write to a file
    with open('professor_ratings_by_subject.txt', 'w', encoding='utf-8') as outfile:
        for prof in subject_professors:
            outfile.write(f"Professor: {prof['name']}\n")
            outfile.write(f"Total Reviews Count: {prof['count']}\n")
            outfile.write(f"Average Rating: {prof['average_rating']:.2f}\n")
            outfile.write("Courses Taught:\n")
            for course in prof['courses']:
                outfile.write(f"\t{course['code']} - {course['name']} (Reviews Count: {course['count']}, Average Rating: {course['avg_rating']:.2f})\n")
            outfile.write("------\n")

    # Display the same results
    for prof in subject_professors:
        print(f"Professor: {prof['name']}")
        print(f"Total Reviews Count: {prof['count']}")
        print(f"Average Rating: {prof['average_rating']:.2f}")
        print("Courses Taught:")
        for course in prof['courses']:
            print(f"\t{course['code']} - {course['name']} (Reviews Count: {course['count']}, Average Rating: {course['avg_rating']:.2f})")
        print("------")


def display_ratings(course_codes = []):
    # Load the details from the json file
    with open("assets/instructor_details.json", 'r', encoding='utf-8') as infile:
        instructor_details = json.load(infile)

    subject_professors = []

    for instructor, details in instructor_details.items():
        relevant_courses = []

        if course_codes:
            relevant_courses = [course for course in details['courses'] if course['code'] in course_codes]
        else:
            relevant_courses = [course for course in details['courses']]
        
        if relevant_courses:
            subject_professors.append({
                'name': instructor,
                'bayes_rating': details['bayes_rating'],
                'average_rating': details['average_rating'],
                'count': details['count'],
                'courses': relevant_courses
            })

    # Sort professors by average rating in descending order
    subject_professors.sort(key=lambda x: x['bayes_rating'], reverse=True)

    # Write to a file
    with open('assets/instructor_ratings.txt', 'w', encoding='utf-8') as outfile:
        for prof in subject_professors:
            outfile.write(f"Instructor: {prof['name']}\n")
            outfile.write(f"Bayes Rating: {prof['bayes_rating']}\n")
            outfile.write(f"Total Reviews Count: {prof['count']}\n")
            outfile.write(f"Average Rating: {prof['average_rating']:.2f}\n")
            outfile.write("Courses Taught:\n")
            for course in prof['courses']:
                outfile.write(f"\t{course['code']} - {course['name']} (Reviews Count: {course['count']}, Average Rating: {course['avg_rating']:.2f})\n")
            outfile.write("------\n")

    # Display the same results
    for prof in subject_professors:
        print(f"Instructor: {prof['name']}")
        print(f"Bayes Rating: {prof['bayes_rating']}")
        print(f"Total Reviews Count: {prof['count']}")
        print(f"Average Rating: {prof['average_rating']:.2f}")
        print("Courses Taught:")
        for course in prof['courses']:
            print(f"\t{course['code']} - {course['name']} (Reviews Count: {course['count']}, Average Rating: {course['avg_rating']:.2f})")
        print("------")

# Usage:
#subject = input("Enter the subject code (e.g., COMP): ")
#display_subject_professors_ratings(subject)

display_ratings(['CORE1401', 'CORE1402', 'CORE1403A', 'CORE1403I', 'CORE1403S', 'CORE1404', 'LANG1002A', 'LANG1002I', 'LANG1002S', 'LANG1003A', 'LANG1003I', 'LANG1003S'])
#Process_Instructor_Info.calculate_instructor_details()
#display_ratings()