import numpy as np

numbers = [10, 20, 30, 40, 50]
array_numbers = np.array([10, 20, 30, 40, 50])

print("Python List:", numbers)
print("NumPy Array:", array_numbers)
print("List size:", len(numbers))
print("Array size:", array_numbers.size)
print("List memory usage:", numbers.__sizeof__())
print("Array memory usage:", array_numbers.nbytes)
print("List operation example:", [x * 2 for x in numbers])
print("Array operation example:", array_numbers * 2)
