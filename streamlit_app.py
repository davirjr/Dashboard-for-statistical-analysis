import altair as alt
import pandas as pd
import streamlit as st
import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kruskal, ranksums

# Show the page title and description.
st.set_page_config(page_title="Dashboard for Statistical Analysis", page_icon="📈", layout="wide")
st.title("Statistical Analysis of New Delhi Food delivery")
st.write(
    """
For this project, I used data from a Kaggle dataset - https://www.kaggle.com/datasets/romanniki/food-delivery-cost-and-profitability. The goal of this project is to demonstrate how to apply statistical analyses in a simple way for everyday use, utilizing Python.

This dashboard provides a method for applying comparative statistics to visual elements. It first performs a Kruskal-Wallis test on all independent variables related to delivery time. If a significant difference is found, a Wilcoxon test is made available to compare each variable individually. The Wilcoxon test will always return two variables from the column that show significant differences, indicating whether the delivery time is greater or lesser. The dashboard then hides all Wilcoxon tests for variables without significant differences.

Kruskal-Wallis tests can be shown by clicking the side button, and each variable in the Wilcoxon test can be changed to test other possibilities.  """
)

# Load the data from a CSV. We're caching this so it doesn't reload every time the app reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data():
    df = pd.read_csv("/workspaces/Dashboard-for-statistical-analysis/food_orders_processed.csv")
    return df

df = load_data()

# Checking the number of days in the DataFrame
df["Day"] = df["Order Date and Time"].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').date() if isinstance(x, str) else x.date())

# Sidebar date input widgets
start_date = st.sidebar.date_input("Start Date", value=datetime.date(2024, 1, 1))
end_date = st.sidebar.date_input("End Date", value=datetime.date(2024, 2, 7))

# Sidebar hour input widget
start_hour = st.sidebar.selectbox("Start Hour", list(range(24)), index=0)
end_hour = st.sidebar.selectbox("End Hour", list(range(24)), index=23)

# Convert the date columns in the DataFrame to datetime format
df["Order Date and Time"] = pd.to_datetime(df["Order Date and Time"])
df["Day"] = pd.to_datetime(df["Day"])

# Filter the DataFrame based on the selected dates and hours
filtered_df = df[(df["Day"] >= pd.to_datetime(start_date)) & 
                 (df["Day"] <= pd.to_datetime(end_date)) &
                 (df["Order Date and Time"].dt.hour >= start_hour) &
                 (df["Order Date and Time"].dt.hour <= end_hour)]

# Sidebar checkbox to show or hide Kruskal-Wallis tests
show_kruskal_wallis = st.sidebar.checkbox('Show Kruskal-Wallis Tests', value=False)

# Kruskal-Wallis test for each column related to "Delivery Time (minutes)"
columns_to_test = ['Restaurant ID', 'Order Date and Time', 'Delivery Date and Time', 'Order Value', 'Delivery Fee', 'Payment Method', 'Discounts and Offers', 'Commission Fee', 'Payment Processing Fee', 'Refunds/Chargebacks']
significant_columns = []

results = {}
for column in columns_to_test:
    groups = [group['Delivery Time (minutes)'].dropna().values for name, group in filtered_df.groupby(column)]
    stat, p_value = kruskal(*groups)
    results[column] = (stat, p_value)
    if p_value < 0.05:
        significant_columns.append(column)

# Define the common significance level
alpha = 0.05

# Display results with interpretation for Kruskal-Wallis test
if show_kruskal_wallis:
    for column, (stat, p_value) in results.items():
        significance = "statistically significant difference" if p_value < alpha else "not statistically significant difference"
        st.write(f"Kruskal-Wallis test for {column} (P-value: {p_value:.2f}): {significance}.")

# Wilcoxon test if Kruskal-Wallis shows significant difference
for column in significant_columns:
    st.sidebar.write(f"Wilcoxon Test for {column}")
    unique_values = filtered_df[column].unique()
    selected_values = st.sidebar.multiselect(f'Select 2 options from {column}', unique_values, default=unique_values[:2])
    
    if len(selected_values) == 2:
        group1 = filtered_df[filtered_df[column] == selected_values[0]]['Delivery Time (minutes)']
        group2 = filtered_df[filtered_df[column] == selected_values[1]]['Delivery Time (minutes)']
        
        # Manually performing the Wilcoxon test
        stat, p_value = ranksums(group1, group2)
        
        # Determine if the median of group1 is greater than or less than group2
        direction = "greater" if group1.median() > group2.median() else "less"
        
        # Format the Wilcoxon test result
        significance = "difference statistically significant" if p_value < alpha else "difference not statistically significant"
        wilcoxon_result = f"Wilcoxon test for {column} between {selected_values[0]} and {selected_values[1]} (P-value: {p_value:.2f}): {significance} and {direction}."

        # Display the result with increased text size, red text color, and black background
        st.markdown(f"""
            <div style="font-size:24px; color:red; background-color:black; padding:10px;">
                {wilcoxon_result}
            </div>
        """, unsafe_allow_html=True)
    
    else:
        st.write(f"Please select exactly two options from {column} for the Wilcoxon test.")

# Add code for the 3rd quartile + EWMA - Day
# 1. Convert 'Delivery Date and Time' to datetime objects and extract the date
filtered_df['Delivery Date'] = pd.to_datetime(filtered_df['Delivery Date and Time']).dt.date

# 2. Group by 'Delivery Date' and calculate the 3rd quartile for each day
daily_quartiles = filtered_df.groupby('Delivery Date')['Delivery Time (minutes)'].quantile(0.75).reset_index()

# 3. Calculate EWMA for the 3rd quartile
daily_quartiles['EWMA'] = daily_quartiles['Delivery Time (minutes)'].ewm(alpha=0.3, adjust=False).mean()  # Adjust alpha as needed

# 4. Plot the 3rd quartile and EWMA
plt.figure(figsize=(12, 6))
plt.plot(daily_quartiles['Delivery Date'], daily_quartiles['Delivery Time (minutes)'], label='3rd Quartile', marker='o')
plt.plot(daily_quartiles['Delivery Date'], daily_quartiles['EWMA'], label='EWMA', color='red')
plt.title('3rd Quartile and EWMA by Day')
plt.xlabel('Delivery Date')
plt.ylabel('Delivery Time (minutes)')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
plt.tight_layout()
st.pyplot(plt)

# Add code for the 3rd quartile + EWMA - Hour
# 1. Convert 'Delivery Date and Time' to datetime objects and extract the hour
filtered_df['Delivery Hour'] = pd.to_datetime(filtered_df['Delivery Date and Time']).dt.hour

# 2. Group by 'Delivery Hour' and calculate the 3rd quartile and count for each hour
hourly_data = filtered_df.groupby('Delivery Hour').agg(
    Quartile=('Delivery Time (minutes)', lambda x: x.quantile(0.75)),
    Count=('Delivery Time (minutes)', 'count')
).reset_index()

# 3. Calculate EWMA for the 3rd quartile
hourly_data['EWMA'] = hourly_data['Quartile'].ewm(alpha=0.3, adjust=False).mean()  # Adjust alpha as needed

# 4. Plot the 3rd quartile, EWMA, and delivery count
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot 3rd quartile and EWMA on the primary y-axis (ax1)
ax1.plot(hourly_data['Delivery Hour'], hourly_data['Quartile'], label='3rd Quartile', marker='o')
ax1.plot(hourly_data['Delivery Hour'], hourly_data['EWMA'], label='EWMA', color='red')
ax1.set_xlabel('Hour of the Day')
ax1.set_ylabel('Delivery Time (minutes)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Create a secondary y-axis (ax2) for delivery count
ax2 = ax1.twinx()

# Plot delivery count as bars on the secondary y-axis (ax2)
bar_width = 0.5  # Adjust bar width as needed
ax2.bar(hourly_data['Delivery Hour'], hourly_data['Count'], label='Delivery Count', width=bar_width, color='green', alpha=0.5)  # Added alpha for transparency
ax2.set_ylabel('Delivery Count', color='green')
ax2.tick_params(axis='y', labelcolor='green')

# Set x-axis ticks to represent hours of the day, align bar centers with ticks
ax2.set_xticks(np.arange(24))

# Adjust layout, set title, and show the plot
fig.tight_layout()
plt.title('3rd Quartile, EWMA, and Delivery Count by Hour of the Day')

# Combine legends from both axes
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')  # Adjust legend location if needed

st.pyplot(fig)