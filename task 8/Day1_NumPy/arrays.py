import numpy as np

arr_1d = np.array([1, 2, 3])
arr_2d = np.array([[1, 2], [3, 4]])
arr_3d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])

arrays = [arr_1d, arr_2d, arr_3d]
for index, arr in enumerate(arrays, start=1):
    print(f"Array {index}:")
    print(arr)
    print("Dimensions:", arr.ndim)
    print("Shape:", arr.shape)
    print("Data Type:", arr.dtype)
    print("Size:", arr.size)
    print()
