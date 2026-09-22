import numpy as np

arr = np.array([[10, 20, 30], [40, 50, 60]])

print("First element:", arr[0, 0])
print("Last element:", arr[1, 2])
print("Middle element:", arr[0, 1])
print("First row:", arr[0])
print("Second column:", arr[:, 1])
print("Multiple values:", arr[0, :])
