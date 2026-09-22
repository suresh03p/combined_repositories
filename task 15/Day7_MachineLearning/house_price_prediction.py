from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

base_dir = Path(__file__).resolve().parent
data_dir = base_dir / "data"
model_dir = base_dir / "models"
chart_dir = base_dir / "charts"
for directory in (data_dir, model_dir, chart_dir):
    directory.mkdir(exist_ok=True, parents=True)

# Create 100-house dataset
np.random.seed(42)
num_houses = 100

area = np.random.randint(800, 3500, size=num_houses)
bedrooms = np.random.randint(1, 6, size=num_houses)
bathrooms = np.random.randint(1, 4, size=num_houses)
age = np.random.randint(0, 25, size=num_houses)
parking = np.random.randint(0, 3, size=num_houses)

# Price formula
price = (
    area * 2600
    + bedrooms * 600000
    + bathrooms * 700000
    - age * 25000
    + parking * 350000
    + np.random.normal(0, 250000, size=num_houses)
)

# Create DataFrame
house_df = pd.DataFrame({
    "House_ID": np.arange(1, num_houses + 1),
    "Area_sqft": area,
    "Bedrooms": bedrooms,
    "Bathrooms": bathrooms,
    "Age": age,
    "Parking": parking,
    "Price": price.round(2),
})

# Save dataset to CSV
csv_path = data_dir / "house_prices.csv"
house_df.to_csv(csv_path, index=False)
print(f"Dataset saved to {csv_path}")
print(house_df.head())

# Check missing values, duplicates, and data types
print("\nMissing values:\n", house_df.isnull().sum())
print("\nDuplicate records:", house_df.duplicated().sum())
print("\nData types:\n", house_df.dtypes)

# Separate features and target
X = house_df[["Area_sqft", "Bedrooms", "Bathrooms", "Age", "Parking"]]
y = house_df["Price"]

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on test data
predictions = model.predict(X_test)

# Evaluate model
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\nMAE:", mae)
print("MSE:", mse)
print("R²:", r2)

# Save model
model_path = model_dir / "house_price_model.pkl"
joblib.dump(model, model_path)
print(f"\nSaved model to {model_path}")

# Visualize
plt.figure(figsize=(8, 5))
plt.scatter(y_test, predictions, color="blue")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color="red", linestyle="--")
plt.title("Actual vs Predicted House Price")
plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.grid(True)
plt.tight_layout()
chart_path = chart_dir / "actual_vs_predicted.png"
plt.savefig(chart_path)
plt.show()

# Test loaded model
loaded_model = joblib.load(model_path)
new_house = [[1800, 3, 2, 4, 2]]
new_prediction = loaded_model.predict(new_house)[0]
print("\nPredicted price for new house (Area=1800, Bedrooms=3, Bathrooms=2, Age=4, Parking=2):", round(new_prediction, 2))
print("\nConclusion:")
print("This model learns the relationship between house attributes and price.")
print("It can estimate prices for new houses after training on historical examples.")
