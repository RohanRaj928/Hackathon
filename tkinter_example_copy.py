import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import random

def floatToString(inputValue):
    return ('%.15f' % inputValue).rstrip('0').rstrip('.')

# --- Load CSV Data ---
def load_csv_data():
    csv_data = {}
    with open('dataset.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = row['Timestamp']
            s1_emissions = round(float(row['Scope_1_Emissions_tonnes_CO2e']))
            s2_emissions = round(float(row['Scope_2_Emissions_tonnes_CO2e']))
            renewable_percentage = round(float(row['On_Site_Renewable_Energy_Percentage']))
            csv_data[date] = {'s1_emissions': s1_emissions, 's2_emissions': s2_emissions, 'renewable_percentage': renewable_percentage}
    return csv_data

csv_data = load_csv_data()

# --- Simulated API Call for s2 Emissions ---
def get_s2_emissions(day_index, location):
    """
    Simulates retrieving the s2 emissions based on location.
    For this example, s2 emissions are computed as: fixed s1 emissions (150) + 20 + (day_index * 5) + location factor.
    """
    location_factor = location_factors[location]
    return round(150 + 20 + (day_index * 5) + location_factor)

# --- Update Week Info ---
def update_week_info(start_date):
    global week_info
    week_info = []
    for i in range(7):
        date = start_date + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        day_name = date.strftime("%A")
        if date_str in csv_data:
            s1_emissions = csv_data[date_str]['s1_emissions']
            s2_emissions = csv_data[date_str]['s2_emissions']
            renewable_percentage = csv_data[date_str]['renewable_percentage']
        else:
            s1_emissions = round(random.uniform(100, 200)) if date == datetime.now().date() else '???'
            s2_emissions = round(random.uniform(100, 200)) if date == datetime.now().date() else '???'
            renewable_percentage = '???'
        week_info.append({'day_name': day_name, 'date_str': date_str, 's1_emissions': s1_emissions, 's2_emissions': s2_emissions, 'renewable_percentage':renewable_percentage})
    update_day_frames()

# --- Update Day Frames ---
def update_day_frames():
    for i, day_info in enumerate(week_info):
        day_labels[i].config(text=f"{day_info['day_name']} ({day_info['date_str']})")
        s1_radio_buttons[i].config(text=f"s1 ({day_info['s1_emissions']} tonnes CO2)")
        s2_radio_buttons[i].config(text=f"s2 ({day_info['s2_emissions']} tonnes CO2)")

# --- Calculation Function ---
def calculate_cost_difference():
    total_cost = 0
    result_text = "CO2 Emissions Difference Breakdown:\n\n"

    # Loop through each day and compute the cost difference based on the selected option.
    for i, day_info in enumerate(week_info):
        selection = day_vars[i].get()  # either "s1" or "s2"
        day_name = day_info['day_name']
        date_str = day_info['date_str']

        emissions = day_info['s1_emissions'] + day_info['s2_emissions']
        renewable_percentage = day_info['renewable_percentage']

        cost = emissions * 16.20
        result_text += f"{day_name} ({date_str}): Total Emissions = {emissions} tonnes CO2, Cost = £{round(cost)}, Percentage Renewable: = {renewable_percentage}%\n\n"
        total_cost += cost

    result_text += f"\nTotal = £{total_cost}"
    result_label.config(text=result_text)

    # Update the Matplotlib graph
    update_graph()

# --- Update Graph ---
def update_graph():
    s1_emissions = [day_info['s1_emissions'] for day_info in week_info]
    s2_emissions = [day_info['s2_emissions'] for day_info in week_info]
    days = [day_info['day_name'] for day_info in week_info]

    fig, ax = plt.subplots()
    ax.plot(days, s1_emissions, label='s1 Emissions')
    ax.plot(days, s2_emissions, label='s2 Emissions')
    ax.set_xlabel('Days')
    ax.set_ylabel('Emissions (tonnes CO2)')
    ax.set_title('Emissions Comparison')
    ax.legend()

    # Clear the previous canvas if it exists
    for widget in graph_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# --- Main Application ---
root = tk.Tk()
root.title("CO2 Emissions Calculator")

# --- Apply Green Forestry Theme ---
style = ttk.Style()
style.theme_use('clam')

style.configure('TLabel', background='#e0f7e0', foreground='#004d00', font=('Arial 12 bold', 14))
style.configure('TButton', background='#004d00', foreground='#ffffff', font=('Arial 12 bold', 14))
style.configure('TRadiobutton', background='#e0f7e0', foreground='#004d00', font=('Arial 12 bold', 14))
style.configure('TCombobox', background='#e0f7e0', foreground='#004d00', font=('Arial 12 bold', 14))
style.configure('TFrame', background='#e0f7e0')

root.configure(background='#e0f7e0')

# --- Location Factors ---
location_factors = {
    "Cameronbridge": 0,
    "Blackgrange": 10,
    "Glenkinchie": 20
}

# --- Selected Location ---
selected_location = tk.StringVar(value="Cameronbridge")

# --- Location Dropdown ---
location_frame = ttk.Frame(root)
location_frame.pack(pady=5)

location_label = ttk.Label(location_frame, text="Select Location:")
location_label.pack(side='left', padx=5)
location_dropdown = ttk.Combobox(location_frame, textvariable=selected_location, values=list(location_factors.keys()))
location_dropdown.pack(side='left', padx=5)

# --- Reset to Current Date ---
def reset_to_current_date():
    cal.selection_set(datetime.now())
    update_week_info(datetime.now())

reset_button = ttk.Button(root, text="Reset to Current Date", command=reset_to_current_date)
reset_button.pack(pady=5)

# --- Calendar Widget ---
cal = Calendar(root, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
cal.pack(pady=20)

# --- Center Frame for Option Selection ---
center_frame = ttk.Frame(root)
center_frame.pack(pady=20)

# --- Week Info ---
week_info = []
day_labels = []
day_vars = []
s1_radio_buttons = []
s2_radio_buttons = []

# --- Initialize Week Info ---
def initialize_week_info():
    start_date = datetime.now()
    update_week_info(start_date)

# --- Option Selection ---
s1_label = ttk.Label(center_frame, text="S1")
s1_label.grid(row=1, column=0, padx=10, pady=5)
s2_label = ttk.Label(center_frame, text="S2")
s2_label.grid(row=2, column=0, padx=10, pady=5)

for i in range(7):
    day_frame = ttk.Frame(center_frame)
    day_frame.grid(row=0, column=i+1, padx=10, pady=5)

    day_label = ttk.Label(day_frame, text="")
    day_label.pack(side='top', padx=5)
    day_labels.append(day_label)

    var = tk.StringVar(value='s1')
    day_vars.append(var)

    s1_radio = ttk.Radiobutton(center_frame, text='s1', variable=var, value='s1')
    s1_radio.grid(row=1, column=i+1, padx=5)
    s1_radio_buttons.append(s1_radio)

    s2_radio = ttk.Radiobutton(center_frame, text='s2', variable=var, value='s2')
    s2_radio.grid(row=2, column=i+1, padx=5)
    s2_radio_buttons.append(s2_radio)

# --- Update Week Info on Date Change ---
def on_date_change(event):
    selected_date = cal.selection_get()
    update_week_info(selected_date)

cal.bind("<<CalendarSelected>>", on_date_change)

# --- Update Week Info on Location Change ---
def on_location_change(event):
    update_week_info(cal.selection_get())

location_dropdown.bind("<<ComboboxSelected>>", on_location_change)

# --- Calculate Button ---
calculate_button = ttk.Button(root, text="Calculate Cost Difference", command=calculate_cost_difference)
calculate_button.pack(pady=20)

# --- Result and Graph Frame ---
result_graph_frame = ttk.Frame(root)
result_graph_frame.pack(pady=20, fill='x')

# --- Result Label ---
result_label = ttk.Label(result_graph_frame, text="", justify='left', font=('Arial', 14))
result_label.grid(row=0, column=0, padx=10)

# --- Graph Frame ---
graph_frame = ttk.Frame(result_graph_frame)
graph_frame.grid(row=0, column=1, padx=10)

# --- Initialize Week Info ---
initialize_week_info()

# --- Run the Application ---
root.mainloop()
