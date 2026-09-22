import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May"]
sales = [12000, 15000, 18000, 14000, 22000]

# 1. Line Chart
plt.figure(figsize=(8, 5))
plt.plot(months, sales, marker='o', linestyle='-', color='green')
plt.title('Line Chart: Monthly Sales')
plt.xlabel('Month')
plt.ylabel('Sales (USD)')
plt.grid(True, linestyle='--', alpha=0.4)
plt.savefig('charts/chart_types_line_chart.png', dpi=150, bbox_inches='tight')
plt.close()

# 2. Bar Chart
plt.figure(figsize=(8, 5))
plt.bar(months, sales, color='skyblue')
plt.title('Bar Chart: Monthly Sales')
plt.xlabel('Month')
plt.ylabel('Sales (USD)')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.savefig('charts/chart_types_bar_chart.png', dpi=150, bbox_inches='tight')
plt.close()

# 3. Scatter Plot
plt.figure(figsize=(8, 5))
plt.scatter(months, sales, color='red', s=80)
plt.title('Scatter Plot: Monthly Sales')
plt.xlabel('Month')
plt.ylabel('Sales (USD)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig('charts/chart_types_scatter_plot.png', dpi=150, bbox_inches='tight')
plt.close()

# 4. Histogram
plt.figure(figsize=(8, 5))
plt.hist(sales, bins=5, color='purple', edgecolor='black')
plt.title('Histogram: Sales Distribution')
plt.xlabel('Sales (USD)')
plt.ylabel('Frequency')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.savefig('charts/chart_types_histogram.png', dpi=150, bbox_inches='tight')
plt.close()

# 5. Pie Chart
plt.figure(figsize=(7, 7))
plt.pie(sales, labels=months, autopct='%1.1f%%', startangle=140)
plt.title('Pie Chart: Sales Share by Month')
plt.savefig('charts/chart_types_pie_chart.png', dpi=150, bbox_inches='tight')
plt.close()

if __name__ == '__main__':
    print('chart_types.py ran successfully and saved 5 charts in charts/')
