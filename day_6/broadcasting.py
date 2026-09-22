import numpy as np

# What is broadcasting?
# Broadcasting is NumPy's ability to perform arithmetic operations on arrays of different shapes.
# It expands the smaller array automatically to match the shape of the larger one.

# Why AI Engineers use broadcasting?
# - It enables vectorized operations and avoids Python loops.
# - It is faster and more memory efficient for large tensor operations.
# - It simplifies code for element-wise math across arrays.

# Array + Number
arr = np.array([1, 2, 3])
print("Array:", arr)
print("Array + 5:", arr + 5)
print()

# Array × Number
print("Array * 3:", arr * 3)
print()

# NumberArray + Array (scalar broadcast)
scalar = 10
print("Scalar + Array:", scalar + arr)
print()

# Matrix + Vector
matrix = np.array([[1, 2, 3], [4, 5, 6]])
vector = np.array([10, 20, 30])
print("Matrix:")
print(matrix)
print("Vector:", vector)
print("Matrix + Vector:")
print(matrix + vector)
print()

# Compatible broadcasting example
matrix2 = np.array([[1], [2], [3]])
print("Matrix2:")
print(matrix2)
print("Matrix2 + arr:")
print(matrix2 + arr)
