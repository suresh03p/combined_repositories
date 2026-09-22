# Missing Value Report

## Missing Values Found
- Missing values were present in `Age`, `Salary`, `Experience`, `Email`, and `City`.
- Some missing values were caused by blank cells or invalid numeric strings.

## Methods Compared

1. **dropna()**
   - Drops any row containing a missing value.
   - Best for datasets where missing rows are few and non-critical.
   - Drawback: can remove too much data if many rows have at least one missing value.

2. **fillna() with mean**
   - Replaces missing numeric values with the average of that column.
   - Best when the data is roughly symmetric and there are no strong outliers.
   - Drawback: mean can be affected by extreme values.

3. **fillna() with median**
   - Replaces missing numeric values with the median of that column.
   - Best when numeric data is skewed or contains outliers.
   - Drawback: may ignore distribution shape and consistency across groups.

4. **fillna() with mode**
   - Replaces missing categorical values with the most frequent category.
   - Best for categorical fields with a common default value.
   - Drawback: can reinforce an existing class imbalance.

5. **forward fill and backward fill**
   - Propagate nearby values to fill missing cells.
   - Best for ordered or time-series data where neighbor values are meaningful.
   - Drawback: not ideal for unstructured or independent records.

## Which Method is Better?
- There is no single best method. The best choice depends on the dataset and the meaning of missing values.
- For this HR dataset, median imputation for numeric columns is a strong choice because it is robust to outliers.
- For categorical columns, using mode or a placeholder value is preferable to preserve rows.

## When to Use Each Method
- Use `dropna()` when missing data is minimal and records are not important.
- Use `fillna(mean)` when the column distribution is approximately normal.
- Use `fillna(median)` when the distribution is skewed or contains outliers.
- Use `fillna(mode)` for categorical fields where a common category is valid.
- Use `ffill` or `bfill` for time-series or sequence data where nearby values are relevant.
