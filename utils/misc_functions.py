"""
File: misc_functions.py
Author: Aidan McEnaney
Date: 2023-08-11

Description: Module containing misc functions.

Contents:
    - get_timeslots: Function that turns start and end data into date tuples.
    - kelvin_to_fahrenheit: Function that converts Kelvin to Fahrenheit.

Notes:
    - This code is distributed under the MIT License. See LICENSE.txt for more details.
"""

# Standard library imports


# Third-party library imports


# Local module imports


def get_timeslots(start, end, n_chunks):
    """
    Divide a time period into equal-sized time slots.

    Args:
        start (datetime): Start datetime of the time period.
        end (datetime): End datetime of the time period.
        n_chunks (int): Number of equal-sized time slots.

    Returns:
        list of tuple: List of tuples representing start and end datetime for each time slot.
    """

    tdelta = (end - start) / n_chunks
    edges = [(start + i * tdelta).date().isoformat() for i in range(n_chunks)]
    date_tuples = [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]

    return date_tuples

def kelvin_to_fahrenheit(kelvin):
    """
    Convert temperature in Kelvin to Fahrenheit.

    Args:
        kelvin (float): Temperature in Kelvin.

    Returns:
        float: Temperature in Fahrenheit.
    """

    fahrenheit = (kelvin - 273.15) * 9/5 + 32
    return fahrenheit