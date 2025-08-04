students ={
    "59VOV":{"name": "Kelvin","Attendance": 5,"status":"Eligible"},
    "60AB7":{"name": "Oketch","Attendance": 4,"status":"Eligible"},
    "90DC2":{"name": "Vivian","Attendance": 3,"status":"Eligible"},
    "70XY8":{"name": "Otieno","Attendance": 6,"status":"Eligible"},
}
upin = input("Enter studentt's UPIN!:")

if upin in students:
    students[upin]["Attendance"] +=1

    #check if attendance reaches 4 or more
    if students[upin]["Attendance"] >= 4:
        students[upin]["status"] = "Eligible"
    else:
        print("student is not legible to sit for the EXAMS!")

subject = ["Maths", "Programming", "Digital Literacy", "AI Fundamentals"]

grades = {}
total = 0

for subject in subjects:
    mark = int(input(f"Enter marks for {subject}:"))
    grades[subject] = mark
    total += mark

    average = total / len(subject)

if average >= 50:
    exam_status = "pass"
    print("grade = C ")
else:
    exam_status = "supplementary"

students[upin]["grade"] = grades
students[upin]["average"] = average
students[upin]["exam_status"] = exam_status  








