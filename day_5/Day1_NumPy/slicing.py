import numpy as np

arr = np.array([10, 20, 30, 40, 50, 60])

print("First 3 elements:", arr[:3])
print("Last 2 elements:", arr[-2:])
print("Middle values:", arr[2:5])
print("Entire row:", arr[:])
print("Reverse array:", arr[::-1])

arr2 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("First row:", arr2[0, :])
print("Second column:", arr2[:, 1])
print("Submatrix:", arr2[0:2, 1:3])
print("Elements 2 to 4:", arr[1:4])
print("Every second element:", arr[::2])
