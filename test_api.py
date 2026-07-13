import requests
import json
import uuid
import random
import string
from datetime import datetime, timedelta

# --- Configuration ---
BASE_URL = "http://127.0.0.1:8080"
ADMIN_EMAIL = "youremail@gmail.com"  # REPLACE WITH YOUR ACTUAL ADMIN EMAIL
ADMIN_PASSWORD = "your@admin@password123FswSf"  # REPLACE WITH YOUR ACTUAL ADMIN PASSWORD

# --- High-Volume Configuration ---
NUM_DIRECTORS = 2
NUM_TEACHERS = 20
NUM_STUDENTS = 200
NUM_CLASSES_PER_SCHOOL = 15
NUM_SUBJECTS_PER_SCHOOL = 10
NUM_GRADES_TO_CREATE = 1500
NUM_SCHEDULES_TO_CREATE = 200

# --- Data Pools for Realistic Names ---
FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph",
    "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy",
    "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra"
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson"
]
SUBJECT_NAMES = [
    "Algebra I", "Geometry", "Calculus", "Biology", "Chemistry", "Physics",
    "World History", "American History", "European History", "English Literature",
    "Creative Writing", "Spanish I", "Spanish II", "French I", "German I",
    "Studio Art", "Art History", "Music Theory", "Band", "Orchestra", "Choir",
    "Physical Education", "Health", "Computer Science", "Digital Media"
]
SCHOOL_PREFIXES = ["North", "South", "East", "West", "Central", "Upper", "Lower", "Saint", "Mount", "Fort"]
SCHOOL_SUFFIXES = ["High School", "Academy", "Institute", "Preparatory School", "College"]

# --- Global Storage for IDs ---
resource_ids = {
    "main_school_id": None,
    "student_user_ids": [],
    "actual_student_entry_ids": [],
    "director_user_ids": [],
    "teacher_user_ids": [],
    "school_class_ids": [],
    "school_subject_ids": [],
    "student_credentials": [],
    "teacher_credentials": [],
    "director_credentials": [],  # Added for director login
    "grade_ids": [],
    "used_schedule_slots": set()
}


# --- Helper Functions ---
def generate_unique_email(first_name, last_name):
    return f"{first_name.lower()}.{last_name.lower()}_{uuid.uuid4().hex[:4]}@example.com"


def generate_random_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.ascii_lowercase)
    ]
    password += random.choices(chars, k=random.randint(5, 10))
    random.shuffle(password)
    return "".join(password)


def make_request(method, path, test_name, token=None, json_data=None, expected_status=200, suppress_errors=False):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"{BASE_URL}{path}"
    response_json = None
    test_passed = False
    try:
        response = requests.request(method, url, headers=headers, json=json_data)
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            response_json = None

        if response.status_code == expected_status:
            test_passed = True
        else:
            if not suppress_errors:
                print(f"Result: FAILED (Expected {expected_status}, Got {response.status_code}) for {test_name}")
                print(f"Status Code: {response.status_code}")
                if response_json:
                    print(f"Response: {json.dumps(response_json, indent=2)}")
                else:
                    print(f"Response (non-JSON): {response.text}")
            test_passed = False
    except requests.exceptions.ConnectionError:
        if not suppress_errors:
            print(f"Result: FAILED (Connection Error - Is the Flask app running at {BASE_URL}?) for {test_name}")
        test_passed = False
    except Exception as e:
        if not suppress_errors:
            print(f"Result: FAILED (An unexpected error occurred: {e}) for {test_name}")
        test_passed = False

    return response_json, test_passed


# --- Main Test Script ---
def run_tests():
    print("Starting API high-volume stress test...")
    admin_token = None
    test_results = []

    # 1. Admin Login
    test_name = "Admin Login"
    print(f"\n--- Attempting {test_name} ---")
    login_payload = {"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    response_data, passed = make_request("POST", "/login", test_name, json_data=login_payload, expected_status=200)
    test_results.append({"name": test_name, "passed": passed})

    if response_data and "token" in response_data:
        admin_token = response_data["token"]
        print("Admin login successful. Token obtained.")
    else:
        print("Admin login failed. Cannot proceed.")
        return

    # --- Test Routes ---

    # Create one main school
    print(f"\n--- Creating the main school ---")
    school_name = f"{random.choice(SCHOOL_PREFIXES)} {random.choice(SCHOOL_SUFFIXES)}"
    school_address = f"{random.randint(100, 999)} {random.choice(LAST_NAMES)} Street"
    school_payload = {"name": school_name, "institution_address": school_address}
    response_data, passed = make_request("POST", "/school/add", "Create Main School", token=admin_token,
                                         json_data=school_payload, expected_status=200)
    test_results.append({"name": "Create Main School", "passed": passed})

    # Fetch the created school's ID
    schools_data, passed = make_request("GET", "/schools/list", "Fetch Schools", token=admin_token, expected_status=200)
    if schools_data:
        main_school_info = next((s for s in schools_data if s['name'] == school_name), None)
        if main_school_info:
            resource_ids["main_school_id"] = main_school_info['id']
            print(f"Main school '{school_name}' created with ID: {resource_ids['main_school_id']}")
        else:
            print("Error: Could not find the newly created main school in the list.")
            return
    else:
        print("Error: Could not fetch schools list.")
        return

    # Register users
    print(f"\n--- Registering {NUM_DIRECTORS} directors, {NUM_TEACHERS} teachers, and {NUM_STUDENTS} students ---")
    user_types_to_create = [("director", NUM_DIRECTORS), ("teacher", NUM_TEACHERS), ("student", NUM_STUDENTS)]
    for user_type, count in user_types_to_create:
        for i in range(count):
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            email = generate_unique_email(first_name, last_name)
            password = generate_random_password()
            register_payload = {"first_name": first_name, "last_name": last_name, "email": email, "password": password}

            response_data, passed = make_request("POST", "/register", f"Register {user_type} {i + 1}",
                                                 json_data=register_payload, expected_status=201, suppress_errors=True)
            test_results.append({"name": f"Register {user_type} {i + 1}", "passed": passed})

            if passed and response_data and "id" in response_data:
                user_id = response_data["id"]
                if user_type == "student":
                    resource_ids["student_user_ids"].append(user_id)
                    resource_ids["student_credentials"].append({"email": email, "password": password, "id": user_id})
                elif user_type == "director":
                    resource_ids["director_user_ids"].append(user_id)
                    resource_ids["director_credentials"].append({"email": email, "password": password, "id": user_id})
                elif user_type == "teacher":
                    resource_ids["teacher_user_ids"].append(user_id)
                    resource_ids["teacher_credentials"].append({"email": email, "password": password, "id": user_id})
    print("User registration complete.")

    # Log credentials for one of each type
    print("\n--- Sample Credentials for Manual Login ---")
    if resource_ids["student_credentials"]:
        print(f"Student Email: {resource_ids['student_credentials'][0]['email']}")
        print(f"Student Password: {resource_ids['student_credentials'][0]['password']}")
    if resource_ids["teacher_credentials"]:
        print(f"Teacher Email: {resource_ids['teacher_credentials'][0]['email']}")
        print(f"Teacher Password: {resource_ids['teacher_credentials'][0]['password']}")
    if resource_ids["director_credentials"]:
        print(f"Director Email: {resource_ids['director_credentials'][0]['email']}")
        print(f"Director Password: {resource_ids['director_credentials'][0]['password']}")

    # Assign roles to the main school
    print("\n--- Assigning roles to the main school ---")
    for director_id in resource_ids["director_user_ids"]:
        payload = {"director_id": director_id, "school_id": resource_ids["main_school_id"]}
        make_request("POST", "/principle/add", "Assign Director", token=admin_token, json_data=payload,
                     expected_status=200, suppress_errors=True)

    for teacher_id in resource_ids["teacher_user_ids"]:
        payload = {"teacher_id": teacher_id, "school_id": resource_ids["main_school_id"]}
        make_request("POST", "/teacher/add", "Assign Teacher", token=admin_token, json_data=payload,
                     expected_status=200, suppress_errors=True)
    print("Role assignment complete.")

    # Create classes and subjects for the main school
    print(f"\n--- Creating {NUM_CLASSES_PER_SCHOOL} classes and {NUM_SUBJECTS_PER_SCHOOL} subjects ---")
    for i in range(NUM_CLASSES_PER_SCHOOL):
        class_payload = {"grade": random.randint(1, 12), "letter": random.choice(string.ascii_uppercase),
                         "school_id": resource_ids["main_school_id"]}
        make_request("POST", "/school/class/add", f"Create Class {i + 1}", token=admin_token, json_data=class_payload,
                     expected_status=201, suppress_errors=True)

    for i in range(NUM_SUBJECTS_PER_SCHOOL):
        subject_payload = {"name": random.choice(SUBJECT_NAMES), "school_id": resource_ids["main_school_id"]}
        make_request("POST", "/school/subject/add", f"Create Subject {i + 1}", token=admin_token,
                     json_data=subject_payload, expected_status=201, suppress_errors=True)

    # Fetch all class and subject IDs for the main school
    classes_data, _ = make_request("GET", f"/school/{resource_ids['main_school_id']}/classes", "Fetch Classes",
                                   token=admin_token)
    if classes_data: resource_ids["school_class_ids"] = [c["id"] for c in classes_data]

    subjects_data, _ = make_request("GET", f"/school/{resource_ids['main_school_id']}/subjects", "Fetch Subjects",
                                    token=admin_token)
    if subjects_data: resource_ids["school_subject_ids"] = [s["id"] for s in subjects_data]
    print(
        f"Created {len(resource_ids['school_class_ids'])} classes and {len(resource_ids['school_subject_ids'])} subjects.")

    # Enroll students in classes
    print("\n--- Enrolling students in classes ---")
    if resource_ids["student_user_ids"] and resource_ids["school_class_ids"]:
        for student_id in resource_ids["student_user_ids"]:
            class_id = random.choice(resource_ids["school_class_ids"])
            payload = {"class_id": class_id, "student_id": student_id}
            _, passed = make_request("POST", "/student/add-to-class", "Enroll Student", token=admin_token,
                                     json_data=payload, expected_status=201, suppress_errors=True)
            if passed:
                resource_ids["actual_student_entry_ids"].append(student_id)
    print(f"Enrolled {len(resource_ids['actual_student_entry_ids'])} students.")

    # Create schedules
    print(f"\n--- Creating {NUM_SCHEDULES_TO_CREATE} schedule entries ---")
    if all([resource_ids["school_class_ids"], resource_ids["school_subject_ids"], resource_ids["teacher_user_ids"]]):
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for i in range(NUM_SCHEDULES_TO_CREATE):
            class_id = random.choice(resource_ids["school_class_ids"])
            day_of_week = random.choice(days_of_week)
            start_time_str = f"{random.randint(8, 16):02d}:{random.choice(['00', '30'])}"

            attempts = 0
            while (class_id, day_of_week, start_time_str) in resource_ids["used_schedule_slots"] and attempts < 50:
                class_id = random.choice(resource_ids["school_class_ids"])
                day_of_week = random.choice(days_of_week)
                start_time_str = f"{random.randint(8, 16):02d}:{random.choice(['00', '30'])}"
                attempts += 1
            if attempts == 50: continue

            resource_ids["used_schedule_slots"].add((class_id, day_of_week, start_time_str))
            start_dt = datetime.strptime(start_time_str, "%H:%M")
            end_dt = start_dt + timedelta(hours=1)
            end_time_str = end_dt.strftime("%H:%M")

            schedule_payload = {
                "day_of_week": day_of_week, "start_time": start_time_str, "end_time": end_time_str,
                "class_number": random.randint(1, 8), "room_number": random.randint(101, 599),
                "class_id": class_id,
                "subject_id": random.choice(resource_ids["school_subject_ids"]),
                "teacher_id": random.choice(resource_ids["teacher_user_ids"])
            }
            make_request("POST", "/schedule/add", f"Create Schedule {i + 1}", token=admin_token,
                         json_data=schedule_payload, expected_status=201, suppress_errors=True)
    print("Schedule creation complete.")

    # Log in as a teacher to add grades
    teacher_token = None
    if resource_ids["teacher_credentials"]:
        random_teacher = random.choice(resource_ids["teacher_credentials"])
        teacher_login_payload = {"email": random_teacher["email"], "password": random_teacher["password"]}
        teacher_login_response, _ = make_request("POST", "/login", "Teacher Login", json_data=teacher_login_payload,
                                                 expected_status=200)
        if teacher_login_response and "token" in teacher_login_response:
            teacher_token = teacher_login_response["token"]
            print("\nLogged in as a random teacher to add grades.")

    # Add a large number of grades
    print(f"\n--- Adding {NUM_GRADES_TO_CREATE} grades ---")
    if all([teacher_token, resource_ids["actual_student_entry_ids"], resource_ids["school_subject_ids"]]):
        for i in range(NUM_GRADES_TO_CREATE):
            grade_payload = {
                "student_id": random.choice(resource_ids["actual_student_entry_ids"]),
                "subject_id": random.choice(resource_ids["school_subject_ids"]),
                "teacher_id": random.choice(resource_ids["teacher_user_ids"]),
                "grade": random.randint(2, 6),
                "comment": f"Performance on the {random.choice(SUBJECT_NAMES)} quiz was satisfactory."
            }
            make_request("POST", "/grade/add", f"Create Grade {i + 1}", token=teacher_token, json_data=grade_payload,
                         expected_status=201, suppress_errors=True)
    print("Grade creation complete.")

    # --- Final Summary ---
    print("\nHigh-volume stress test finished.")

    # A simple count of total requests made can be estimated.
    total_requests = 1 + 1 + (
                NUM_DIRECTORS + NUM_TEACHERS + NUM_STUDENTS) + NUM_CLASSES_PER_SCHOOL + NUM_SUBJECTS_PER_SCHOOL + len(
        resource_ids["student_user_ids"]) + NUM_SCHEDULES_TO_CREATE + NUM_GRADES_TO_CREATE + 2
    print(f"Approximately {total_requests} requests were made.")


if __name__ == "__main__":
    run_tests()