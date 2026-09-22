import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


df = pd.DataFrame({
    "Age": [25, 30, 28, 35, 31, 42],
    "Experience": [2, 5, 4, 10, 6, 15],
    "City": ["Hyderabad", "Chennai", "Hyderabad", "Bangalore", "Chennai", "Bangalore"],
    "Salary": [30000, 50000, 45000, 80000, 60000, 100000],
})
X, y = df.drop(columns="Salary"), df["Salary"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
numeric = X.select_dtypes(include=["number"]).columns.tolist()
categorical = X.select_dtypes(include=["object"]).columns.tolist()
preprocessor = ColumnTransformer([
    ("numeric", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), numeric),
    ("categorical", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("encoder", OneHotEncoder(handle_unknown="ignore"))]), categorical),
])
model = Pipeline([("preprocessing", preprocessor), ("model", LinearRegression())])
model.fit(X_train, y_train)
print("Predictions:", model.predict(X_test))
print("Workflow complete: split -> identify -> impute -> encode/scale -> train -> predict.")