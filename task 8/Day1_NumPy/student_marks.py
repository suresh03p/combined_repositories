import numpy as np

marks = np.array([
    [78, 82, 90, 88, 85],
    [72, 76, 80, 79, 81],
    [88, 91, 87, 84, 86],
    [65, 70, 75, 72, 74],
    [95, 93, 97, 96, 94],
])

print("Student marks matrix:")
print(marks)

print("\nTotal Marks:", np.sum(marks))
print("Average Marks:", np.mean(marks))
print("Highest Score:", np.max(marks))
print("Lowest Score:", np.min(marks))
print("Class Average:", np.mean(marks))
print("Student Wise Average:", np.mean(marks, axis=1))
print("Subject Wise Average:", np.mean(marks, axis=0))
