from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "employees.csv"
MODEL_PATH = ROOT / "models" / "employee_salary_pipeline.pkl"
REPORT_PATH = ROOT / "reports" / "model_evaluation.md"
FEATURES = ["Age", "Gender", "City", "Department", "Education", "Experience", "Performance_Score"]


def create_dataset(path=DATA_PATH, rows=520):
    rng = np.random.default_rng(8)
    cities = ["Hyderabad", "Chennai", "Bangalore", "Mumbai", "Delhi"]
    departments = ["IT", "HR", "Finance", "Sales", "Operations"]
    education = ["Bachelor's", "Master's", "PhD"]
    frame = pd.DataFrame({
        "Employee_ID": [f"E{i:04d}" for i in range(1, rows + 1)],
        "Age": rng.integers(21, 61, rows), "Gender": rng.choice(["Male", "Female"], rows),
        "City": rng.choice(cities, rows), "Department": rng.choice(departments, rows),
        "Education": rng.choice(education, rows, p=[0.55, 0.35, 0.10]),
        "Experience": rng.integers(0, 26, rows), "Performance_Score": rng.integers(1, 11, rows),
    })
    frame["Salary"] = (28000 + frame["Experience"] * 4200 + frame["Performance_Score"] * 3200
                        + frame["Age"] * 350 + rng.normal(0, 5000, rows)).round(2)
    frame.loc[[7, 44, 121], "Salary"] = np.nan
    frame.loc[[18, 90], "Age"] = np.nan
    frame.loc[30, "City"] = " hyderabad "
    frame = pd.concat([frame, frame.iloc[[10, 20]]], ignore_index=True)
    path.parent.mkdir(exist_ok=True)
    frame.to_csv(path, index=False)
    return frame


def clean_data(frame):
    frame = frame.drop_duplicates().copy()
    for column in ["Gender", "City", "Department", "Education"]:
        frame[column] = frame[column].astype("string").str.strip().replace({"<NA>": np.nan})
    frame["City"] = frame["City"].str.title()
    frame = frame.dropna(subset=["Salary"])
    return frame


def build_pipeline(X):
    numeric = X.select_dtypes(include=["number"]).columns.tolist()
    categorical = X.select_dtypes(include=["object", "string"]).columns.tolist()
    numeric_steps = Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())])
    categorical_steps = Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("encoder", OneHotEncoder(handle_unknown="ignore"))])
    preprocessing = ColumnTransformer([("numeric", numeric_steps, numeric), ("categorical", categorical_steps, categorical)])
    return Pipeline([("preprocessing", preprocessing), ("model", LinearRegression())])


def main():
    raw = pd.read_csv(DATA_PATH) if DATA_PATH.exists() else create_dataset()
    df = clean_data(raw)
    X, y = df[FEATURES], df["Salary"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    model = build_pipeline(X_train)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    metrics = {"MAE": mean_absolute_error(y_test, predictions), "MSE": mean_squared_error(y_test, predictions), "R2": r2_score(y_test, predictions)}
    MODEL_PATH.parent.mkdir(exist_ok=True)
    REPORT_PATH.parent.mkdir(exist_ok=True)
    pd.to_pickle(model, MODEL_PATH)
    REPORT_PATH.write_text("# Employee Salary Pipeline Evaluation\n\n" + "\n".join(f"- **{key}:** {value:,.4f}" for key, value in metrics.items()) + "\n\nThe pipeline fits imputation, encoding, and scaling on training data only.\n", encoding="utf-8")
    new_employee = pd.DataFrame([{ "Age": 29, "Gender": "Male", "City": "Hyderabad", "Department": "IT", "Education": "Bachelor's", "Experience": 5, "Performance_Score": 8 }])
    print(f"Rows: {len(df)} | Train: {len(X_train)} | Test: {len(X_test)}")
    print("MAE: {MAE:,.2f} | MSE: {MSE:,.2f} | R2: {R2:.4f}".format(**metrics))
    print(f"Predicted Salary: {model.predict(new_employee)[0]:,.2f}")


if __name__ == "__main__":
    main()