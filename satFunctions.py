## Aidan McEnaney
## June 30th, 2023
## Functions used in the satellite image analysis code


## Imports

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io
import datetime
import os
from utils import plot_image
import math

## End of Imports

def plot_ndarrays(ndarrays, titles, coordinates, num_columns=3):
    if len(ndarrays) != len(titles):
        raise ValueError("Number of ndarrays and titles must be the same.")

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
    plt.show()

def convert_to_celsius(temperature_array):
    temperature_celsius = temperature_array - 273.15
    return temperature_celsius

def convert_to_fahrenheit(temperature_array):
    temperature_fahrenheit = (temperature_array * 9/5) - 459.67
    return temperature_fahrenheit

def get_timeslots(start, end, n_chunks):
    tdelta = (end - start) / n_chunks
    edges = [(start + i * tdelta).date().isoformat() for i in range(n_chunks)]
    slots = [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]

    return slots
