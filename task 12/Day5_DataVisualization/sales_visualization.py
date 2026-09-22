import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random
from datetime import datetime, timedelta

# Generate a sales dataset with 100 records.
products = ['Laptop', 'Phone', 'Headphones', 'Monitor', 'Keyboard', 'Mouse', 'Printer']
categories = ['Electronics', 'Accessories']
regions = ['North', 'South', 'East', 'West']
start_date = datetime(2024, 1, 1)

records = []
for i in range(1, 101):
    date = start_date + timedelta(days=random.randint(0, 180))
    product = random.choice(products)
    category = 'Electronics' if product in ['Laptop', 'Phone', 'Monitor', 'Printer'] else 'Accessories'
    region = random.choice(regions)
    quantity = random.randint(1, 10)
    price = random.randint(50, 1500)
    revenue = quantity * price
    records.append({
        'Order_ID': f'ORD{i:03d}',
        'Date': date,
        'Product': product,
        'Category': category,
        'Region': region,
        'Quantity': quantity,
        'Price': price,
        'Revenue': revenue
    })

df = pd.DataFrame(records)
df.to_csv('data/sales.csv', index=False)

# Sales metrics
print('Total Revenue:', df['Revenue'].sum())
print('Average Revenue:', df['Revenue'].mean())
print('Highest Revenue:', df['Revenue'].max())
print('Lowest Revenue:', df['Revenue'].min())

print('Best-selling Product:', df.groupby('Product')['Quantity'].sum().idxmax())
print('Worst-selling Product:', df.groupby('Product')['Quantity'].sum().idxmin())
print('Best Region:', df.groupby('Region')['Revenue'].sum().idxmax())
print('Lowest-performing Region:', df.groupby('Region')['Revenue'].sum().idxmin())

# 1. monthly_sales.png
monthly = df.set_index('Date').resample('ME')['Revenue'].sum().reset_index()
monthly['Date'] = monthly['Date'].dt.strftime('%Y-%m')
plt.figure(figsize=(10, 5))
sns.lineplot(x='Date', y='Revenue', data=monthly, marker='o')
plt.title('Monthly Sales Revenue')
plt.xlabel('Month')
plt.ylabel('Revenue (USD)')
plt.xticks(rotation=45)
plt.savefig('charts/monthly_sales.png', dpi=150, bbox_inches='tight')
plt.close()

# 2. product_sales.png
product_sales = df.groupby('Product')['Revenue'].sum().reset_index()
plt.figure(figsize=(10, 5))
sns.barplot(x='Product', y='Revenue', data=product_sales, palette='tab10')
plt.title('Revenue by Product')
plt.xlabel('Product')
plt.ylabel('Revenue (USD)')
plt.savefig('charts/product_sales.png', dpi=150, bbox_inches='tight')
plt.close()

# 3. region_sales.png
region_sales = df.groupby('Region')['Revenue'].sum().reset_index()
plt.figure(figsize=(8, 5))
sns.barplot(x='Region', y='Revenue', data=region_sales, palette='Set2')
plt.title('Revenue by Region')
plt.xlabel('Region')
plt.ylabel('Revenue (USD)')
plt.savefig('charts/region_sales.png', dpi=150, bbox_inches='tight')
plt.close()

# 4. revenue_distribution.png
plt.figure(figsize=(8, 5))
sns.histplot(df['Revenue'], bins=10, color='purple')
plt.title('Revenue Distribution')
plt.xlabel('Revenue (USD)')
plt.ylabel('Frequency')
plt.savefig('charts/revenue_distribution.png', dpi=150, bbox_inches='tight')
plt.close()

# 5. quantity_distribution.png
plt.figure(figsize=(8, 5))
sns.histplot(df['Quantity'], bins=10, color='green')
plt.title('Quantity Distribution')
plt.xlabel('Quantity')
plt.ylabel('Frequency')
plt.savefig('charts/quantity_distribution.png', dpi=150, bbox_inches='tight')
plt.close()

# 6. price_distribution.png
plt.figure(figsize=(8, 5))
sns.histplot(df['Price'], bins=10, color='orange')
plt.title('Price Distribution')
plt.xlabel('Price (USD)')
plt.ylabel('Frequency')
plt.savefig('charts/price_distribution.png', dpi=150, bbox_inches='tight')
plt.close()

# 7. revenue_vs_quantity.png
plt.figure(figsize=(8, 5))
sns.scatterplot(x='Quantity', y='Revenue', hue='Category', data=df, palette='deep', s=100)
plt.title('Revenue vs Quantity')
plt.xlabel('Quantity')
plt.ylabel('Revenue (USD)')
plt.savefig('charts/revenue_vs_quantity.png', dpi=150, bbox_inches='tight')
plt.close()

# 8. category_sales.png
category_sales = df.groupby('Category')['Revenue'].sum().reset_index()
plt.figure(figsize=(8, 5))
sns.barplot(x='Category', y='Revenue', data=category_sales, palette='dark')
plt.title('Revenue by Category')
plt.xlabel('Category')
plt.ylabel('Revenue (USD)')
plt.savefig('charts/category_sales.png', dpi=150, bbox_inches='tight')
plt.close()

# 9. region_comparison.png
plt.figure(figsize=(8, 5))
sns.boxplot(x='Region', y='Revenue', data=df, palette='pastel')
plt.title('Revenue Distribution by Region')
plt.xlabel('Region')
plt.ylabel('Revenue (USD)')
plt.savefig('charts/region_comparison.png', dpi=150, bbox_inches='tight')
plt.close()

# 10. correlation_heatmap.png
corr = df[['Quantity', 'Price', 'Revenue']].corr()
plt.figure(figsize=(6, 5))
sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Sales Data Correlation Heatmap')
plt.savefig('charts/correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()

if __name__ == '__main__':
    print('sales_visualization.py ran successfully and generated data/sales.csv and 10 chart images in charts/')
