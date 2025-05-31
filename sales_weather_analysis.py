import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sales_excel_filepath = r"C:\Users\sshik\hello\13_project\Coffee Shop Sales.csv"
weather_excel_filepath = r"C:\Users\sshik\hello\13_project\Combined_Weather_Data.csv"

try:
	# Load sales data
	sales_data = pd.read_csv(sales_excel_filepath)
	print(sales_data)
	# Load weather data
	weather_data = pd.read_csv(weather_excel_filepath)
	print(weather_data)
except FileNotFoundError:
	print("There's no such file.")
finally:
	print("Try-Catch Performed!")

# Convert sales_data date columns to datetime
sales_data['date'] = pd.to_datetime(sales_data['date'], dayfirst=True).dt.date

# Renaming store_location to Location
sales_data.rename(columns={'store_location': 'Location'}, inplace=True)

# Convert weather_data date columns to datetime
weather_data['date'] = pd.to_datetime(weather_data['date']).dt.date

# Merge both file on date and Location
merged_data = pd.merge(sales_data, weather_data, on=['date', 'Location'], how='left')
print("\n Merged data ",merged_data)

# Save combined data
merged_data.to_csv("Merged_Sales_Weather_Data.csv", index=False)
print("Merged data saved!")

# Info about data
print("\n Info ")
print(merged_data.info())

# Description of data
print("\n Describe ")
print(merged_data.describe())

# Null values
print("\n Null values ")
print(merged_data.isnull().sum())

# Calculate total_price
merged_data['total_price'] = merged_data['transaction_qty'] * merged_data['unit_price']
print(merged_data)

# Added Temp Categories Column
temp_bins = [0, 40, 65, 100]
temp_labels = ['Cold', 'Mild', 'Hot']
merged_data['temp_range'] = pd.cut(merged_data['temp'], bins=temp_bins, labels=temp_labels)

# Added day_of_week column by extracting date
merged_data['day_of_week'] = pd.to_datetime(merged_data['date']).dt.day_name()
print(merged_data)


# Visualizations
# 1. Sales trend over time
daily_sales = merged_data.groupby('date')['total_price'].sum().reset_index()
plt.figure(figsize=(8,5))
sns.lineplot(data=daily_sales, x='date', y='total_price')
plt.title("Sales Trend Over Time")
plt.xlabel("Date")
plt.ylabel("Total Sales")
plt.show()

# 2. Weather Impact on Sales (temp vs total_price)
weather_sales = merged_data.groupby('date').agg({'total_price':'sum', 'temp': 'mean'}).reset_index()
plt.figure(figsize=(8,5))
sns.scatterplot(data=weather_sales, x='temp', y='total_price', alpha=0.6)
plt.title("Temperature vs. Sales")
plt.xlabel("Temperature")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.show()

# 3. Sales by Product Category & Weather Condition
category_weather = merged_data.groupby(['product_category','conditions'])['total_price'].sum().unstack().fillna(0)
# Add total column for sorting
category_weather['total'] = category_weather.sum(axis=1)
# Sort by total and drop 'total' before plotting
category_weather = category_weather.sort_values('total', ascending=False).drop(columns='total')
category_weather.plot(kind='bar', stacked=True)
plt.title("Sales by Product Category & Weather Condition")
plt.ylabel('Sales Amount')
plt.xlabel('Product Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. Top performing store & location
top_performing_store = merged_data.groupby('Location')['total_price'].sum().sort_values(ascending=False)
sns.barplot(x=top_performing_store.values, y=top_performing_store.index)
plt.title("Top Performing Location")
plt.ylabel("Store Location")
plt.xlabel("Total Sales")
plt.yticks(rotation=45)
plt.tight_layout()
plt.show()

# 5. Sales During Different Times(hours) of Day
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# Convert day_of_week column to categorical with correct order
merged_data['day_of_week'] = pd.Categorical(merged_data['day_of_week'], categories=day_order, ordered=True)
day_sales = merged_data.groupby('day_of_week')['total_price'].sum().reset_index()
sns.lineplot(data=day_sales, x='day_of_week', y='total_price', marker='o')
plt.title("Sales by Week")
plt.xlabel('Week')
plt.ylabel('Sales')
plt.tight_layout()
plt.show()

# 6. Top Performing Weather
# Group by weather condition and calculate average sales
weather_avg_sales = merged_data.groupby('conditions')['total_price'].sum().sort_values(ascending=False)
# Get the top weather condition
top_weather = weather_avg_sales.idxmax()
top_value = weather_avg_sales.max()

print(f"Top-Performing Weather: {top_weather} with Sum. Sales of ${top_value:.2f}")

