import numpy as np

class_mean = 60
std_dev = 10
student_score = 80
z_score = (student_score - class_mean) / std_dev

print("Class Average:", class_mean)
print("Standard Deviation:", std_dev)
print("Student Score:", student_score)
print("Z-score:", z_score)
print("Interpretation: The student is 2 standard deviations above the mean.")
print("This means the student is above average.")

# 20 student marks
marks = [45, 50, 52, 58, 60, 62, 64, 66, 68, 70,
         72, 74, 75, 77, 79, 80, 82, 85, 90, 95]
mean_marks = np.mean(marks)
std_marks = np.std(marks)
zs = [(m, (m - mean_marks) / std_marks) for m in marks]

print("\n20 Student Marks:", marks)
print("Mean:", mean_marks)
print("Standard Deviation:", std_marks)
print("Z-scores:")
for mark, z in zs:
    print(f"  Mark {mark}: Z = {z:.2f}")

highest = max(zs, key=lambda x: x[1])
lowest = min(zs, key=lambda x: x[1])
print("\nHighest Z-score:", highest)
print("Lowest Z-score:", lowest)
print("Students significantly above average: marks above 1 standard deviation from mean")
print("Students significantly below average: marks below 1 standard deviation from mean")
