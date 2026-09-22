import numpy as np

# Convert 1D -> 2D
arr1d = np.arange(6)
print("Original 1D array:", arr1d)
print("Original shape:", arr1d.shape)
arr2d = arr1d.reshape((2, 3))
print("Reshaped to 2D:")
print(arr2d)
print("New shape:", arr2d.shape)
print("Number of elements:", arr2d.size)
print()

# Convert 2D -> 3D
arr2d_b = np.arange(12).reshape((3, 4))
print("Original 2D array:")
print(arr2d_b)
print("Original shape:", arr2d_b.shape)
arr3d = arr2d_b.reshape((2, 2, 3))
print("Reshaped to 3D:")
print(arr3d)
print("New shape:", arr3d.shape)
print("Number of elements:", arr3d.size)
print()

# Convert 3D -> 1D
arr3d_c = np.arange(24).reshape((2, 3, 4))
print("Original 3D array shape:", arr3d_c.shape)
arr_flat = arr3d_c.flatten()
print("Flattened array:", arr_flat)
print("Flattened shape:", arr_flat.shape)
print("Number of elements:", arr_flat.size)
print()

# Using ravel()
raveled = arr3d_c.ravel()
print("Raveled array:", raveled)
print("Raveled shape:", raveled.shape)
print("Number of elements:", raveled.size)
print()

# Transpose
arr_transpose = np.arange(6).reshape((2, 3))
print("Original shape:", arr_transpose.shape)
print(arr_transpose)
transposed = arr_transpose.transpose()
print("Transposed shape:", transposed.shape)
print(transposed)
print()

# Resize
arr_resize = np.arange(6)
print("Original array:", arr_resize)
print("Original shape:", arr_resize.shape)
arr_resize.resize((3, 2))
print("Resized array:")
print(arr_resize)
print("New shape:", arr_resize.shape)
print("Number of elements:", arr_resize.size)
