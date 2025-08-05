student = {}

def register_student():
    upin = input("Enter your UPIN: ").upper()
    if upin in students:
        print("❌ A student with this UPIN already exists.\n")
        return

    name = input("Enter your name: ")
    course = input("Enter your course: ")

    students[upin] = {
        "name": name,
        "course": course,
        "Attendance": 0,
        "status": "Not eligible",
        "grades": {},
        "average": 0,
        "exam_status": "Not yet taken"
    }

    print(f"✅ Student {name} registered successfully!\n")

    def login_student():
    upin = input("Enter your UPIN to login: ").upper()
    if upin not in students:
        print("❌ Student not found.\n")
        return

    student = students[upin]
    print("\n--- Student Dashboard ---")
    print(f"Name: {student['name']}")
    print(f"Course: {student['course']}")
    print(f"Attendance: {student['Attendance']}")
    print(f"Eligibility Status: {student['status']}")
    print(f"Average Score: {student['average']}")
    print(f"Exam Status: {student['exam_status']}")
    print("Grades:")
    if student["grades"]:
        for subject, grade in student["grades"].items():
            print(f"  {subject}: {grade}")
    else:
        print("  No exam results yet.\n")

 while True:
    print("\n--- Student System Menu ---")
    print("1. Register Student")
    print("2. Student Login")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        register_student()
    elif choice == "2":
        login_student()
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid choice.\n")       