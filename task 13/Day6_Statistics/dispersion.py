import numpy as np

# Dataset A and B
A = np.array([48, 49, 50, 51, 52])
B = np.array([10, 30, 50, 70, 90])

for name, data in [("Dataset A", A), ("Dataset B", B)]:
    mean_val = np.mean(data)
    range_val = np.max(data) - np.min(data)
    var_val = np.var(data)
    std_val = np.std(data)
    print(f"{name}:")
    print(f"  Mean = {mean_val:.2f}")
    print(f"  Range = {range_val}")
    print(f"  Variance = {var_val:.2f}")
    print(f"  Standard Deviation = {std_val:.2f}")
    print()

print("Both datasets have a similar average, but they are different because the spread of values is different.")
print("Dataset A values are tightly clustered around 50, while Dataset B values are scattered far from the mean.")
print("This shows that different datasets can have the same average but different dispersion.")
