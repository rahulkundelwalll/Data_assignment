import pandas as pd
from datetime import timedelta
import numpy as np  



# I am using .CSV file and also change the name to Assigment.csv
file_path = 'Assignment.csv'
def analyze_work_days(data):
    # Seting the threshold for consecutive work days
    consecutive_days_threshold = 7
    employee_info = []

    for employee, group in data.groupby('Employee Name'):
        # Calculating consecutive days using the difference between Time entries
        consecutive_days = group['Time'].diff().dt.days.fillna(0).eq(1).cumsum()
        # Checking if any group has consecutive days greater than the threshold
        if any(group.groupby(consecutive_days)['Time'].count() >= consecutive_days_threshold):
            employee_info.append(group.iloc[0])

    print("\nEmployees who have worked for 7 consecutive days:")
    with open('output.txt', 'a') as output_file:
        output_file.write("\nEmployees who have worked for 7 consecutive days:")
    print_employee_info(employee_info)

def analyze_shift_times(data):
    # Seting the threshold for minimum and maximum shift times
    min_shift_time = timedelta(minutes=60)
    max_shift_time = timedelta(minutes=840)

    employee_info = []

    for i in range(len(data) - 1):
        current_time_out = data.iloc[i]['Time Out']
        next_time_in = data.iloc[i + 1]['Time']

        time_diff = (next_time_in - current_time_out)

        # Checking if the time difference is within the specified range
        if min_shift_time < time_diff < max_shift_time:
            employee_info.append(data.iloc[i])
            employee_info.append(data.iloc[i + 1])

    print("\nEmployees with less than 10 hours between shifts but greater than 1 hour:")
    with open('output.txt', 'a') as output_file:
        output_file.write("\nEmployees with less than 10 hours between shifts but greater than 1 hour:")
    
    print_employee_info(employee_info)

def analyze_single_shift_hours(data):
    # Setig the threshold for maximum single shift hours
    max_single_shift_hours = timedelta(minutes=840)

    employee_info = []

    for _, row in data.iterrows():
        shift_hours_str = str(row['Timecard Hours (as Time)'])

        # Checking for NULL values
        if shift_hours_str.lower() == 'nan':
            continue

        # Converting the 'hh:mm' to timedelta
        shift_hours = timedelta(hours=int(shift_hours_str.split(':')[0]), minutes=int(shift_hours_str.split(':')[1]))

        # Checking if shift hours exceed the specified threshold
        if shift_hours > max_single_shift_hours:
            employee_info.append(row)

    print("\nEmployees who have worked for more than 14 hours in a single shift:")
    with open('output.txt', 'a') as output_file:
        output_file.write("\nEmployees who have worked for more than 14 hours in a single shift:")
    print_employee_info(employee_info)

def print_employee_info(employee_info):
    with open('output.txt', 'a') as output_file:
        output_file.write("\n\n")
        for row in employee_info:
            employee_info_str = f"Employee Name: {row['Employee Name']}, Position: {row['Position ID']}\n"
            print(employee_info_str)
            output_file.write(employee_info_str)

def main():
    
    
    # Read CSV file into a DataFrame, parsing date columns
    data = pd.read_csv(file_path, parse_dates=['Time', 'Time Out'])

    # Perform analysis on the data
    analyze_work_days(data)
    analyze_shift_times(data)
    analyze_single_shift_hours(data)

if __name__ == "__main__":
    # Clear the content of the output.txt file before running the analysis
    open('output.txt', 'w').close()
    main()
