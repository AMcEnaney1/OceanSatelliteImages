## Aidan McEnaney
## June 30th, 2023
## Functions used for plotting


## Start of imports

import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import satFunctions

## End of imports

## This is where function to create plots and figures can go.
## The included 'utils.py' file is part of the SentinelHub examples and makes for easy plotting, good for testing.


def plot_ndarrays(ndarrays, titles, coordinates, num_columns=3, save_path=None):
    if len(ndarrays) != len(titles):
        raise ValueError("Number of ndarrays and titles must be the same.")

    if save_path and os.path.exists(save_path):
        print(f"Error: File '{save_path}' already exists, continuing.")
        return

    num_plots = len(ndarrays)
    num_rows = (num_plots - 1) // num_columns + 1

    fig, axes = plt.subplots(num_rows, num_columns, figsize=(4 * num_columns, 4 * num_rows))
    axes = axes.ravel()  # Flatten the axes array

    for i, (arr, title) in enumerate(zip(ndarrays, titles)):
        ax = axes[i]

        # Plot the ndarray
        img = ax.imshow(arr)
        ax.set_title(' to '.join(map(str, title)))  # Concatenate the title elements with a '-' character

        # Set the custom coordinate labels
        lon_left, lat_bottom, lon_right, lat_top = coordinates
        x_ticks = np.linspace(0, arr.shape[1] - 1, num=5)
        y_ticks = np.linspace(0, arr.shape[0] - 1, num=5)
        x_labels = np.linspace(lon_left, lon_right, num=5)
        y_labels = np.linspace(lat_bottom, lat_top, num=5)
        ax.set_xticks(x_ticks)
        ax.set_yticks(y_ticks)
        ax.set_xticklabels(["{:.4f}".format(x) for x in x_labels])
        ax.set_yticklabels(["{:.4f}".format(y) for y in y_labels])

        # Rotate x-axis labels by 45 degrees
        ax.tick_params(axis='x', labelrotation=45)

    # Hide any unused subplots
    for j in range(num_plots, num_rows * num_columns):
        fig.delaxes(axes[j])

    plt.tight_layout()

    if (save_path):
        check_path = save_path + '.npy'
        check_path = check_path.split('/')
        check_path = os.path.join(*list(check_path[:len(check_path)]))
        #if (not os.path.exists(save_path)):
        if (not os.path.exists(check_path)):
            satFunctions.create_batch_folders(save_path)
        plt.savefig(save_path)  # Save the figure as an image file

    plt.close()

def plot_csv_data(csv_path, down_path, column_name, ylabel, corner_text, title=None, fah=False):
    xtickCutOff = 20
    corner_text = str(corner_text)

    dates = []
    values = []

    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date_range = row['Date Range']
            start_date = date_range.strip('()').split(',')[0].strip().strip("'")
            dates.append(start_date)
            if (fah):
                values.append(satFunctions.kelvin_to_fahrenheit(float(row[column_name])))
            else:
                values.append(float(row[column_name]))

    plt.plot(dates, values)

    plt.xlabel('Date Range')
    plt.ylabel(ylabel)
    if (not title):
        plt.title(f"{column_name} vs. Date Range")
    else:
        plt.title(title)

    # Adjust the x-tick labeling based on the number of rows in the CSV
    num_rows = len(dates)
    if num_rows > xtickCutOff:
        # Show only every nth tick, adjust the value of n as needed
        n = int(np.ceil(num_rows / xtickCutOff))
        plt.xticks(range(0, num_rows, n), rotation=45, ha='right')
    else:
        plt.xticks(rotation=45, ha='right')

    plt.tight_layout()

    # Generate the output file path
    csv_filename = os.path.basename(csv_path)
    csv_filename = os.path.splitext(csv_filename)[0]
    output_file = os.path.join(down_path, f"{csv_filename}_{column_name}_{fah}.png")

    # Put text in upper right

    plt.text(0.95, 0.95, corner_text, transform=plt.gca().transAxes, va='top', ha='right')

    # Save the plot as an image file
    plt.savefig(output_file)

    # Close the plot to free up resources
    plt.close()
