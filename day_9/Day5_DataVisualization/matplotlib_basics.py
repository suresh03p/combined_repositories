import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May"]
sales = [12000, 15000, 18000, 14000, 22000]

# Create a line chart to show sales over time.
plt.figure(figsize=(8, 5))
plt.plot(months, sales, marker='o', linestyle='-', color='blue', label='Sales')

# Add a title and axis labels.
plt.title('Monthly Sales')
plt.xlabel('Month')
plt.ylabel('Sales (USD)')

# Add gridlines for easier value reading.
plt.grid(True, linestyle='--', alpha=0.5)

# Add legend to explain the plotted series.
plt.legend()

# Save the figure so it can be reviewed without needing a display.
plt.savefig('charts/matplotlib_basics_line_chart.png', dpi=150, bbox_inches='tight')
plt.close()

if __name__ == '__main__':
    print('matplotlib_basics.py ran successfully and saved charts/matplotlib_basics_line_chart.png')
