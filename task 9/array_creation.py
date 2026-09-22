import numpy as np

# np.zeros()
# Syntax: np.zeros(shape, dtype=float)
# Purpose: Create an array filled with zeros.
print("np.zeros((2, 3)):")
print(np.zeros((2, 3)))
print("Real-life example: Initialize a blank image mask or record counts.")
print()

# np.ones()
# Syntax: np.ones(shape, dtype=float)
# Purpose: Create an array filled with ones.
print("np.ones((2, 3)):")
print(np.ones((2, 3)))
print("Real-life example: Create a default weight vector for normalization.")
print()

# np.empty()
# Syntax: np.empty(shape, dtype=float)
# Purpose: Allocate an array without initializing its values.
print("np.empty((2, 3)):")
print(np.empty((2, 3)))
print("Real-life example: Reserve space for sensor data before filling it.")
print()

# np.full()
# Syntax: np.full(shape, fill_value, dtype=None)
# Purpose: Create an array filled with a constant value.
print("np.full((2, 3), 7):")
print(np.full((2, 3), 7))
print("Real-life example: Set a constant calibration offset for all inputs.")
print()

# np.eye()
# Syntax: np.eye(N, M=None, k=0, dtype=float)
# Purpose: Create a 2D array with ones on the diagonal and zeros elsewhere.
print("np.eye(3):")
print(np.eye(3))
print("Real-life example: Construct an identity matrix for linear algebra computations.")
print()

# np.identity()
# Syntax: np.identity(n, dtype=float)
# Purpose: Create a square identity matrix.
print("np.identity(4):")
print(np.identity(4))
print("Real-life example: Use as a base transformation matrix in graphics.")
print()

# np.arange()
# Syntax: np.arange(start, stop, step)
# Purpose: Create a sequence of values with a fixed step.
print("np.arange(0, 10, 2):")
print(np.arange(0, 10, 2))
print("Real-life example: Generate timestamps or index ranges for simulation.")
print()

# np.linspace()
# Syntax: np.linspace(start, stop, num)
# Purpose: Generate a specified number of evenly spaced values.
print("np.linspace(0, 1, 5):")
print(np.linspace(0, 1, 5))
print("Real-life example: Create interpolation points for plotting or signal sampling.")
