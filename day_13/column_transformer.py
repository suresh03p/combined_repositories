import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


df = pd.DataFrame({
    "Age": [25, None, 35], "Salary": [30000, 50000, None],
    "City": ["Hyderabad", "Chennai", None],
})
numeric = ["Age", "Salary"]
categorical = ["City"]
numeric_pipeline = Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())])
categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore")),
])
preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric),
    ("categorical", categorical_pipeline, categorical),
])
print(preprocessor.fit_transform(df).toarray())
print("Numeric: median imputation -> scaling; categorical: mode imputation -> one-hot encoding.")