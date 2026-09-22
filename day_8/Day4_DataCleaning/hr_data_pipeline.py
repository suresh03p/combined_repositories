import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def inspect_data(df: pd.DataFrame) -> None:
    print("Dataset shape:", df.shape)
    print(df.info())
    print(df.describe(include='all'))


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = df.shape[0]
    df = df.drop_duplicates()
    print(f"Removed {before - df.shape[0]} duplicate rows")
    return df


def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")
    df["Experience"] = pd.to_numeric(df["Experience"], errors="coerce")
    df["JoiningDate"] = pd.to_datetime(df["JoiningDate"], errors="coerce")

    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Salary"] = df["Salary"].fillna(df["Salary"].median())
    df["Experience"] = df["Experience"].fillna(df["Experience"].median())
    df["Email"] = df["Email"].fillna("unknown@example.com")
    df["City"] = df["City"].fillna(df["City"].mode()[0])
    return df


def correct_data_types(df: pd.DataFrame) -> pd.DataFrame:
    df["Age"] = df["Age"].astype(int)
    df["Salary"] = df["Salary"].astype(float)
    df["Experience"] = df["Experience"].astype(int)
    df["JoiningDate"] = pd.to_datetime(df["JoiningDate"])
    return df


def calculate_annual_salary(df: pd.DataFrame) -> pd.DataFrame:
    df["AnnualSalary"] = df["Salary"] * 12
    return df


def generate_department_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = df.groupby("Department")["Salary"].agg([
        "mean",
        "max",
        "min",
        "count"
    ]).rename(columns={
        "mean": "AverageSalary",
        "max": "MaxSalary",
        "min": "MinSalary",
        "count": "EmployeeCount"
    }).reset_index()
    return summary


def save_outputs(df: pd.DataFrame, summary: pd.DataFrame) -> None:
    df.to_csv("cleaned_hr_data.csv", index=False)
    summary.to_csv("department_summary.csv", index=False)


def write_quality_report(path: str, df: pd.DataFrame) -> None:
    with open(path, "w") as report:
        report.write("# Data Quality Report\n\n")
        report.write(f"Total rows after cleaning: {df.shape[0]}\n")
        report.write(f"Total columns: {df.shape[1]}\n\n")
        report.write("## Data Type Summary\n")
        report.write(str(df.dtypes))
        report.write("\n\n")
        report.write("## Missing Values\n")
        report.write(str(df.isnull().sum()))
        report.write("\n\n")
        report.write("## Observations\n")
        report.write("- Duplicates were removed.\n")
        report.write("- Missing numeric values were filled with median values.\n")
        report.write("- Missing categorical values were filled with mode or placeholder values.\n")
        report.write("- Data types were corrected for numerical and datetime columns.\n")
        report.write("- Annual salary was calculated from monthly salary.\n")


if __name__ == "__main__":
    df = load_data("employees_dirty.csv")
    inspect_data(df)
    df = remove_duplicates(df)
    df = fill_missing_values(df)
    df = correct_data_types(df)
    df = calculate_annual_salary(df)
    department_summary = generate_department_summary(df)
    save_outputs(df, department_summary)
    write_quality_report("data_quality_report.md", df)
    print("Pipeline complete. Generated cleaned_hr_data.csv, department_summary.csv, and data_quality_report.md")
