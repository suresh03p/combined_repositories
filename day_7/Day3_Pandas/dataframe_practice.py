import pandas as pd

# Create DataFrame from a dictionary
data_dict = {
    'ID': [101, 102, 103, 104, 105],
    'Name': ['Rahul', 'Anjali', 'Kiran', 'Sneha', 'Ajay'],
    'Age': [24, 25, 23, 26, 27],
    'Department': ['IT', 'HR', 'Finance', 'IT', 'Sales'],
    'Salary': [35000, 40000, 38000, 42000, 45000]
}
df_dict = pd.DataFrame(data_dict)
print("DataFrame from dictionary:")
print(df_dict)
print()

# Create DataFrame from a list of dictionaries
list_of_dicts = [
    {'ID': 101, 'Name': 'Rahul', 'Age': 24, 'Department': 'IT', 'Salary': 35000},
    {'ID': 102, 'Name': 'Anjali', 'Age': 25, 'Department': 'HR', 'Salary': 40000},
    {'ID': 103, 'Name': 'Kiran', 'Age': 23, 'Department': 'Finance', 'Salary': 38000},
    {'ID': 104, 'Name': 'Sneha', 'Age': 26, 'Department': 'IT', 'Salary': 42000},
    {'ID': 105, 'Name': 'Ajay', 'Age': 27, 'Department': 'Sales', 'Salary': 45000}
]
df_list_dict = pd.DataFrame(list_of_dicts)
print("DataFrame from list of dictionaries:")
print(df_list_dict)
print()

# Create DataFrame from a list of lists
list_of_lists = [
    [101, 'Rahul', 24, 'IT', 35000],
    [102, 'Anjali', 25, 'HR', 40000],
    [103, 'Kiran', 23, 'Finance', 38000],
    [104, 'Sneha', 26, 'IT', 42000],
    [105, 'Ajay', 27, 'Sales', 45000]
]
columns = ['ID', 'Name', 'Age', 'Department', 'Salary']
df_list_lists = pd.DataFrame(list_of_lists, columns=columns)
print("DataFrame from list of lists:")
print(df_list_lists)
print()

# Print DataFrame details
print("Head of DataFrame:")
print(df_dict.head())
print()
print("Tail of DataFrame:")
print(df_dict.tail())
print()
print("Shape of DataFrame:", df_dict.shape)
print("Columns of DataFrame:", df_dict.columns.tolist())
print("Index of DataFrame:", df_dict.index.tolist())
print("Data types of DataFrame columns:")
print(df_dict.dtypes)
