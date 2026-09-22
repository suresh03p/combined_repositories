import pandas as pd
import numpy as np

# Create Series from a list
list_series = pd.Series([10, 20, 30, 40, 50])
print("Series from list:")
print(list_series)
print()

# Create Series from a tuple
tuple_series = pd.Series((100, 200, 300, 400, 500))
print("Series from tuple:")
print(tuple_series)
print()

# Create Series from a dictionary
dict_series = pd.Series({'a': 1, 'b': 2, 'c': 3})
print("Series from dictionary:")
print(dict_series)
print()

# Create Series from a NumPy array
np_array = np.array([5.5, 6.5, 7.5])
array_series = pd.Series(np_array)
print("Series from NumPy array:")
print(array_series)
print()

# Print values and index for the list series
print("List series values:", list_series.values)
print("List series index:", list_series.index)
print("List series dtype:", list_series.dtype)
print()

# Access the first and last element in the list series
print("First element:", list_series.iloc[0])
print("Last element:", list_series.iloc[-1])
print()

# Slice values from the list series
print("Slice values (index 1 to 3):")
print(list_series[1:4])
print()

# Print values and index for the dictionary series
print("Dictionary series values:", dict_series.values)
print("Dictionary series index:", dict_series.index)
print("Dictionary series dtype:", dict_series.dtype)
print()

# Access first and last element in the dictionary series
print("First element in dict series:", dict_series.iloc[0])
print("Last element in dict series:", dict_series.iloc[-1])
print()

# Slice values from the dictionary series
print("Slice dictionary series (first two items):")
print(dict_series[:2])
