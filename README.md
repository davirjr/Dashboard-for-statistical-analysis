### README

Dashboard: https://dashboard-for-statistical-analysis.streamlit.app/ 

#### Project Title: **Statistical Analysis of New Delhi Food Delivery**

#### Introduction
For this project, I used data from a Kaggle dataset: [Food Delivery Cost and Profitability](https://www.kaggle.com/datasets/romanniki/food-delivery-cost-and-profitability). The goal of this project is to demonstrate how to apply statistical analyses in a simple way for everyday use, utilizing Python.

#### Description
This dashboard provides a method for applying comparative statistics to visual elements. It first performs a Kruskal-Wallis test on all independent variables related to delivery time. If a significant difference is found, a Wilcoxon test is made available to compare each variable individually. The Wilcoxon test will always return two variables from the column that show significant differences, indicating whether the delivery time is greater or lesser. The dashboard then hides all Wilcoxon tests for variables without significant differences. 

#### Features
- **Kruskal-Wallis Tests**: These tests can be shown by clicking the side button, and each variable in the Wilcoxon test can be changed to test other possibilities.
- **Wilcoxon Tests**: The test results will indicate if the delivery time is greater or lesser between the two variables that show significant differences.
- **Interactive Filters**: Users can filter data based on dates and hours.
- **Visualization**: The dashboard includes visual elements like the third quartile and EWMA plots to analyze delivery times over days and hours.

#### Setup and Installation
1. Clone the repository to your local machine.
2. Ensure you have Python installed (version 3.7 or higher).
3. Install the required libraries using the following command:
    ```bash
    pip install -r requirements.txt
    ```
4. Download the dataset from Kaggle and place it in the appropriate directory.

#### How to Run
1. Load the data from the CSV file:
    ```python
    df = pd.read_csv("/path/to/food_orders_processed.csv")
    ```
2. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```
3. Open the provided local URL to interact with the dashboard.

#### Usage
1. Set the start and end dates using the sidebar.
2. Select the start and end hours.
3. Use the checkbox to display Kruskal-Wallis test results.
4. Choose variables for the Wilcoxon test to see detailed comparisons.
5. View visual plots for deeper insights into delivery times.

#### Data Processing
- **Date Conversion**: Dates are converted to datetime objects to ensure accurate filtering and analysis.
- **Filtering**: Data is filtered based on the selected dates and hours.
- **Group by Operations**: Delivery time data is grouped by days and hours for plotting.

#### Visualizations
- **3rd Quartile and EWMA by Day**: Shows the daily third quartile of delivery times and their Exponentially Weighted Moving Average (EWMA).
- **3rd Quartile, EWMA, and Delivery Count by Hour**: Displays hourly delivery times, their EWMA, and the delivery count.

### **Contato**
- Nome: Davi
- Email: davirjr@gmail.com
- LinkedIn: https://www.linkedin.com/in/davi-rodrigues-junior-b1b822b4/
