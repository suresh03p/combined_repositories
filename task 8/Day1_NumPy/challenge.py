import numpy as np

arr = np.arange(1, 101)

even_numbers = arr[arr % 2 == 0]
odd_numbers = arr[arr % 2 != 0]
multiples_of_5 = arr[arr % 5 == 0]
greater_than_50 = arr[arr > 50]
reversed_array = arr[::-1]

print("Even Numbers:", even_numbers)
print("Odd Numbers:", odd_numbers)
print("Multiples of 5:", multiples_of_5)
print("Numbers Greater Than 50:", greater_than_50)
print("Reversed Array:", reversed_array)
print("Sum of All Numbers:", np.sum(arr))
print("Average:", np.mean(arr))
print("Maximum:", np.max(arr))
print("Minimum:", np.min(arr))
