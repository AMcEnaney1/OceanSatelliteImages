## Aidan McEnaney
## June 30th, 2023
## Functions used in the satellite image analysis code


## Imports

import os
import csv
import matplotlib.pyplot as plt
import numpy as np


## End of Imports


def plot_csv_data(csv_path, down_path, column_name):
    dates = []
    values = []

    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date_range = row['Date Range']
            start_date = date_range.strip('()').split(',')[0].strip().strip("'")
            dates.append(start_date)
            values.append(float(row[column_name]))

    plt.plot(dates, values)

    plt.xlabel('Date Range')
    plt.ylabel(column_name)
    plt.title(f"{column_name} vs. Date Range")

    # Adjust the x-tick labeling based on the number of rows in the CSV
    num_rows = len(dates)
    if num_rows > 20:
        # Show only every nth tick, adjust the value of n as needed
        n = int(np.ceil(num_rows / 20))
        plt.xticks(range(0, num_rows, n), rotation=45, ha='right')
    else:
        plt.xticks(rotation=45, ha='right')

    plt.tight_layout()

    # Generate the output file path
    csv_filename = os.path.basename(csv_path)
    csv_filename = os.path.splitext(csv_filename)[0]
    output_file = os.path.join(down_path, f"{csv_filename}_{column_name}.png")

    # Save the plot as an image file
    plt.savefig(output_file)

    # Close the plot to free up resources
    plt.close()
