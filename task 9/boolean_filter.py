import numpy as np

marks = np.array([45, 67, 89, 23, 56, 91, 72, 35, 84, 60])
print("Original marks:", marks)
print("Marks > 50:", marks[marks > 50])
print("Marks < 40:", marks[marks < 40])
print("Marks >= 75:", marks[marks >= 75])
print("Even numbers:", marks[marks % 2 == 0])
print("Odd numbers:", marks[marks % 2 != 0])
print("Between 50 and 80:", marks[(marks > 50) & (marks < 80)])
