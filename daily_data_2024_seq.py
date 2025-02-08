import csv
import pandas as pd
import numpy as np


daily_2024 = "Diageo_Scotland_Full_Year_2024_Daily_Data.csv"

def read_data(csv_file_path):
    return pd.read_csv(csv_file_path, delimiter=',', quotechar='|')


def sort(df : pd.DataFrame, column : str):
    return df.sort_values(by=column)

def total_energy_consumption(df : pd.DataFrame, place, date_lower, date_upper):
    pass

def total_emmision_tones(df : pd.DataFrame, scope, place):
    return  df[df["Site"] == place]["Scope_{}_Emissions_tonnes_CO2e".format(scope)].sum()




df = read_data(daily_2024)
sum = total_emmision_tones(df, 1, "Cameronbridge")
# print(sorted.head())
# print(sorted.tail())

print(sum)

