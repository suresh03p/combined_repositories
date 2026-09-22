import numpy as np

marks = np.array([45, 67, 89, 23, 56, 91, 72, 35, 84, 60])
print("Original marks:", marks)
print("Sorted marks:", np.sort(marks))
print("Highest mark:", np.sort(marks)[-1])
print("Lowest mark:", np.sort(marks)[0])
print("Unique values:", np.unique(marks))
print("Duplicate values:", [x for x in np.unique(marks) if np.sum(marks == x) > 1])
print("Argsort indices:", np.argsort(marks))
