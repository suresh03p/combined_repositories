import numpy as np
from collections import Counter

# Basic dataset
marks = [45, 50, 60, 65, 70, 75, 80]

mean_value = np.mean(marks)
median_value = np.median(marks)
mode_value = Counter(marks).most_common(1)[0][0] if Counter(marks).most_common(1)[0][1] > 1 else None

print("Dataset:", marks)
print("Mean:", round(mean_value, 2))
print("Median:", median_value)
print("Mode:", mode_value)
print("\nMean = Sum of all values / Number of values")
print("Median = Middle value when sorted")
print("Mode = Most frequently occurring value")

# Practice with 10 different datasets
print("\n--- Practice with 10 Different Datasets ---")
datasets = [
    [10, 20, 30, 40, 50],
    [5, 5, 10, 15, 20],
    [2, 4, 6, 8, 10, 12],
    [25, 30, 35, 35, 40],
    [7, 7, 7, 8, 9],
    [100, 200, 300, 400],
    [15, 15, 15, 15, 15],
    [11, 12, 13, 14, 15, 16, 17],
    [45, 48, 50, 52, 55, 60],
    [90, 80, 70, 60, 50, 40]
]

for i, dataset in enumerate(datasets, 1):
    arr = np.array(dataset)
    count = Counter(dataset)
    mode = count.most_common(1)[0][0] if len(count) > 0 else None
    if len(count) == len(dataset):
        mode = "No mode"
    elif count.most_common(1)[0][1] == 1:
        mode = "No mode"
    print(f"Dataset {i}: {dataset}")
    print(f"  Mean = {np.mean(arr):.2f}")
    print(f"  Median = {np.median(arr):.2f}")
    print(f"  Mode = {mode}")

# Important exercise
print("\n--- Important Exercise ---")
exercise = [10, 20, 30, 40, 1000]
print("Dataset:", exercise)
print("Mean:", np.mean(exercise))
print("Median:", np.median(exercise))
print("Why is the mean heavily affected by 1000?")
print("Because the mean uses the sum of all values. The value 1000 is an outlier and makes the total much larger.")
