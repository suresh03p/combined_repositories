# Inspection Notes

- The dataset contains 17 rows and 10 columns.
- Column names are: EmployeeID, FirstName, LastName, Age, Salary, JoiningDate, Department, Experience, Email, City.
- Data types are not fully consistent: `Age` and `Salary` may be read as object because of invalid and missing values.
- `JoiningDate` is currently a string and requires conversion to datetime.
- Missing values exist in `Age`, `Salary`, `Experience`, `Email`, and `City`.
- There are duplicate records for John Doe and Jane Smith.
- Salary values include numeric strings, floats, and a text value (`fifty thousand`).
- Some emails are malformed, but they are still present as strings.
- The dataset contains department names like IT, HR, Finance, Sales, and Marketing.
- Initial inspection shows the need for cleaning missing values, removing duplicates, correcting data types, and standardizing text.
