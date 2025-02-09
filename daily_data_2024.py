from dataclasses import dataclass, fields
import pandas as pd
from datetime import date

daily_2024 = "Diageo_Scotland_Full_Year_2024_Daily_Data.csv"


@dataclass
class FilterQuery:
    # Timestamp : tuple = (date(2024, 1, 1),date(2024, 12, 31))
    Site : tuple = ()
    Total_Energy_Consumption_MWh : tuple = (None,None)
    Scope_1_Emissions_tonnes_CO2e : tuple = (None,None)
    Scope_2_Emissions_tonnes_CO2e : tuple = (None,None)
    Carbon_Intensity_kgCO2e_per_liter : tuple = (None,None)
    On_Site_Renewable_Energy_Percentage : tuple = (None,None)
    Boiler_Efficiency_Percentage : tuple = (None,None)
    Water_Consumption_liters_per_liter : tuple = (None,None)
    Waste_Heat_Recovery_Efficiency_Percentage : tuple = (None,None)
    Fuel_Type_Gas_Usage_GJ : tuple = (None,None)
    Logistics_Carbon_Footprint_kgCO2e_per_km : tuple = (None,None)

    def filter_data(self, data : pd.DataFrame):
        for field in fields(self):
            if not list(filter(lambda x: x != None, getattr(self, field.name))):
                continue

            column = str(field.name)
            field_data = getattr(self, field.name)

            if column == "Site":        # NOTE: only accepts one site filtering currently
                for location in field_data:
                    print(str(location))
                    data = data.loc[data[column] == str(location)]
                continue
            
            data = data[data[column] >= field_data[0]]
            data = data[data[column] <= field_data[1]]

        return data


def read_data(csv_file_path):
    return pd.read_csv(csv_file_path, delimiter=',', quotechar='|')


def sort(df : pd.DataFrame, column : str):
    return df.sort_values(by=column)

def total_energy_consumption(df : pd.DataFrame, place):
    query = FilterQuery(Site=[place])
    return  query.filter_data(df)["Total_Energy_Consumption_MWh"].sum()

def total_co2_by_place(df : pd.DataFrame, scope, place):
    query = FilterQuery(Site=[place])
    return  query.filter_data(df)["Scope_{}_Emissions_tonnes_CO2e".format(scope)].sum()


    
# TESTS

# df = pd.read_csv(daily_2024, delimiter=',', quotechar='|')
# # f = FilterQuery(Site=["Cameronbridge"])
# f = FilterQuery( Site=['Cameronbridge', 'Glenkinchie'])
# # f = FilterQuery( Scope_1_Emissions_tonnes_CO2e=(620.0,630.0))
# new_df = f.filter_data(df)
# print(new_df)



df = read_data(daily_2024)
sum = total_co2_by_place(df, 1, "Cameronbridge")
print(sum)

