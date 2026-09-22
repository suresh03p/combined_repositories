import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler


X = pd.DataFrame({
    "Age": [20, 35, 60],
    "Salary": [20000, 90000, 200000],
    "Experience": [0, 8, 20],
})

standard = StandardScaler()
X_standard = standard.fit_transform(X)
minimum = MinMaxScaler()
X_minmax = minimum.fit_transform(X)
print("StandardScaler (mean approximately 0, standard deviation approximately 1):")
print(pd.DataFrame(X_standard, columns=X.columns))
print("\nMinMaxScaler (each column is rescaled to 0..1):")
print(pd.DataFrame(X_minmax, columns=X.columns))