import numpy as np

np.random.seed(0)
students = [f"Student_{i+1}" for i in range(20)]
subjects = ["Math", "Physics", "Chemistry", "Biology", "English"]
marks = np.random.randint(35, 101, size=(20, 5))

# Student Analysis
student_totals = marks.sum(axis=1)
student_averages = marks.mean(axis=1)
student_highest = marks.max(axis=1)
student_lowest = marks.min(axis=1)

def grade(score):
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"

student_grades = [grade(avg) for avg in student_averages]

# Subject Analysis
subject_averages = marks.mean(axis=0)
subject_highest = marks.max(axis=0)
subject_lowest = marks.min(axis=0)
subject_pass = np.sum(marks >= 40, axis=0)
subject_fail = np.sum(marks < 40, axis=0)

# Overall Analysis
class_topper = students[np.argmax(student_totals)]
lowest_performer = students[np.argmin(student_totals)]
overall_average = marks.mean()
pass_percentage = np.sum(student_averages >= 40) / len(students) * 100
fail_percentage = 100 - pass_percentage

print("Student Performance Dataset")
print("Subjects:", subjects)
print()
print("Student Analysis:")
for i, student in enumerate(students):
    print(f"{student}: Total={student_totals[i]}, Avg={student_averages[i]:.2f}, High={student_highest[i]}, Low={student_lowest[i]}, Grade={student_grades[i]}")
print()
print("Subject Analysis:")
for i, subject in enumerate(subjects):
    print(f"{subject}: Avg={subject_averages[i]:.2f}, High={subject_highest[i]}, Low={subject_lowest[i]}, Passed={subject_pass[i]}, Failed={subject_fail[i]}")
print()
print("Overall Analysis:")
print("Class Topper:", class_topper)
print("Lowest Performer:", lowest_performer)
print("Overall Average:", overall_average)
print(f"Pass Percentage: {pass_percentage:.2f}%")
print(f"Fail Percentage: {fail_percentage:.2f}%")
