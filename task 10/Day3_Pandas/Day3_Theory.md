# Introduction to Pandas

## What is Pandas?
Pandas is a Python library used for data manipulation and analysis. It provides data structures and functions to handle structured data efficiently, especially tabular data such as spreadsheets and CSV files.

## Why is Pandas important?
Pandas is important because it simplifies working with large datasets. It allows fast data cleaning, transformation, aggregation, and analysis with intuitive syntax. This makes it widely used in AI, machine learning, data science, and business analytics.

## Difference between NumPy and Pandas
- NumPy is mainly for numerical operations on arrays and matrices.
- Pandas builds on NumPy and adds labeled data structures, such as Series and DataFrame.
- NumPy is best for math-heavy calculations, while Pandas is best for handling tabular data with different column types.

## What is a Series?
A Series is a one-dimensional labeled array in Pandas. It can hold data of any type, such as integers, strings, or floats. Each element in a Series has an index label.

## What is a DataFrame?
A DataFrame is a two-dimensional labeled data structure in Pandas. It is like a table with rows and columns. Columns can have different data types, and the DataFrame supports operations like filtering, grouping, and joining.

## Where is Pandas used?
Pandas is used in data cleaning, exploratory data analysis, data preprocessing for machine learning, financial analysis, reporting, and automation. It is a common tool in AI/ML pipelines for preparing datasets and extracting insights.

## CSV File
A CSV file is a plain text file that stores tabular data separated by commas. Each row in the file is a record, and each column is separated by a comma. CSV files are easy to create and read in Pandas.

## Excel File
An Excel file is a spreadsheet file used by Microsoft Excel. Pandas can read and write Excel files, making it easy to import data from spreadsheets and export analysis results.

## Interview Questions and Answers
1. What is Pandas?
   - Pandas is a Python library for data manipulation and analysis, providing data structures like Series and DataFrame.
2. Why do data scientists use Pandas?
   - Because Pandas makes data cleaning, transformation, and analysis fast and readable.
3. How is a Series different from a DataFrame?
   - A Series is one-dimensional with a single index, while a DataFrame is two-dimensional with rows and columns.
4. What is the main use of a DataFrame?
   - The main use is to store and analyze tabular data with multiple columns.
5. What function reads a CSV file in Pandas?
   - `pd.read_csv()` reads a CSV file into a DataFrame.
6. How do you save a DataFrame as a new CSV file?
   - Use `df.to_csv('filename.csv', index=False)`.
7. Can Pandas read Excel files?
   - Yes, Pandas can read Excel files with `pd.read_excel()` and write them with `df.to_excel()`.
8. What does `df.head()` do?
   - `df.head()` displays the first five rows of a DataFrame.
9. How can you access a column in a DataFrame?
   - Use `df['column_name']` or `df.column_name`.
10. What is the difference between `loc` and `iloc`?
    - `loc` selects by label/index, while `iloc` selects by integer position.

## Summary
Pandas is a powerful library for working with structured data in Python. It supports reading and writing many file types, making it essential for data science and AI workflows. Learning Series and DataFrames is the first step to using Pandas effectively.