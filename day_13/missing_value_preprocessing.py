import pandas as pd
from sklearn.impute import SimpleImputer


df = pd.DataFrame({
    "Age": [25, 30, None, 35],
    "Salary": [30000, None, 45000, 80000],
    "Experience": [2, 5, 4, None],
})

print("Missing values:\n", df.isnull().sum())
for strategy in ("mean", "median", "most_frequent"):
    filled = pd.DataFrame(
        SimpleImputer(strategy=strategy).fit_transform(df),
        columns=df.columns,
    )
    print(f"\n{strategy.title()} imputation:\n{filled}")

print("\nMean: use for fairly symmetric numerical data without major outliers.")
print("Median: use for skewed numerical data or data containing outliers.")
print("Most frequent: use for categorical or discrete columns.")