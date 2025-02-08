import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

url = 'https://raw.githubusercontent.com/lucadiageo/HeriotWattHackathon/main/Diageo_Scotland_Full_Year_2024_Daily_Data.csv'
data = pd.read_csv(url)

# print(data.head())
# print(data.isnull().sum())
# print(data.describe())


def plot_carbon_emissions(start_date=None, end_date=None):
    url = 'https://raw.githubusercontent.com/lucadiageo/HeriotWattHackathon/main/Diageo_Scotland_Full_Year_2024_Daily_Data.csv'
    data = pd.read_csv(url)

    # Convert the timestamp column to datetime format
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])

    # Filter data based on the given date range
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        data = data[(data['Timestamp'] >= start_date)
                    & (data['Timestamp'] <= end_date)]

    # Group by site and sum carbon emissions
    site_emissions = data.groupby(
        'Site')['Total_Energy_Consumption_MWh'].sum().sort_values(ascending=False)

    # Plot the total carbon emissions per site
    plt.figure(figsize=(12, 6))
    sns.barplot(x=site_emissions.index,
                y=site_emissions.values, palette='coolwarm')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Site')
    plt.ylabel('Total Carbon Emissions (MWh)')
    plt.title('Total Carbon Emissions Per Site')
    plt.show()

    # Plot the carbon emissions over time
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=data, x='Timestamp', y='Total_Energy_Consumption_MWh',
                 hue='Site', marker='o')
    plt.xlabel('Date')
    plt.ylabel('Carbon Emissions (MWh)')
    plt.title('Carbon Emissions Over Time')
    plt.legend(title='Site', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.show()


# Example Usage
plot_carbon_emissions(start_date='2024-01-01', end_date='2024-12-31')
