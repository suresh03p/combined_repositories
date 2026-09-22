# EDA Report

## Business Observations
- The company has employees across IT, HR, Finance, Sales, and Marketing.
- Average salary is moderate, but Finance and IT appear to have higher pay ranges.
- Some roles show very high salaries, indicating a potential need to confirm whether they are executives or outliers.
- Department staffing is uneven, with IT and Finance being the largest groups.

## Data Quality Issues
- Several rows contain missing values in `Age`, `Salary`, `Experience`, `Email`, and `City`.
- Salary values include text and inconsistent numeric formats, causing type conversion issues.
- There are duplicate employee records for John Doe and Jane Smith.
- `JoiningDate` is stored as text and should be converted to datetime.
- Some email addresses are malformed or missing entirely.
- There is an outlier age value of 104, which should be reviewed for accuracy.

## Suggestions for Improvement
- Standardize salary entry formats to numeric values only.
- Use validation when collecting join dates and email addresses.
- Deduplicate records during data entry or import to avoid repeated employees.
- Replace missing values using context-aware imputation or review missing rows manually.
- Add constraints or cleanup rules for age, experience, and department values.
