import pandas as pd
from sklearn.preprocessing import LabelEncoder


ordered = pd.Series(["Low", "Medium", "High", "Medium"], name="Priority")
encoder = LabelEncoder()
print(pd.DataFrame({"Priority": ordered, "Encoded": encoder.fit_transform(ordered)}))
print("Label encoding is suitable here because Low < Medium < High is meaningful.")
print("Do not use it blindly for cities: integer labels would suggest a false ranking.")