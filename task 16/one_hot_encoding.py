import pandas as pd
from sklearn.preprocessing import OneHotEncoder


df = pd.DataFrame({
    "City": ["Hyderabad", "Chennai", "Bangalore", "Hyderabad"],
    "Department": ["IT", "HR", "Finance", "IT"],
    "Gender": ["Female", "Male", "Male", "Female"],
    "Education": ["Bachelor's", "Master's", "Bachelor's", "PhD"],
})
encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
encoded = encoder.fit_transform(df)
encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(df.columns))
print(encoded_df)
print("Each new binary column represents one category, without implying category order.")