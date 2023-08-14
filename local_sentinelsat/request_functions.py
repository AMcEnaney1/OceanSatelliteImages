## Aidan McEnaney
## August 1st, 2023
## Python file to store requests for sentinelsat API

## Start of imports

from datetime import datetime, timedelta
from collections import OrderedDict
from conf.config import *
import utils.misc_functions as mf

## End of imports

def get_olci(date_tuples,  # List of tuples, each containing start and end dates for data retrieval.
             bbox,  # Bounding box coordinates [min_lon, min_lat, max_lon, max_lat].
             download_directory  # Directory where downloaded data will be saved.
             ):
    """
    Downloads multiple OLCI (Ocean and Land Color Instrument) snapshot's data based on the specified parameters.

    Args:
        date_tuples (list): A list of tuples, each containing start and end dates for data retrieval.
        bbox (list): Bounding box coordinates [min_lon, min_lat, max_lon, max_lat].
        download_directory (str): The directory where downloaded data will be saved.

    Returns:
        None
    """

    wkt_bbox = mf.bbox_to_WKT(bbox)

    # Initialize an empty OrderedDict to store the products
    products = OrderedDict()

    for i in range(len(date_tuples)):
        start_date = datetime.strptime(date_tuples[i][0], '%Y-%m-%d')
        end_date = datetime.strptime(date_tuples[i][1], '%Y-%m-%d')

        # Query for products on the earliest date within the date range
        current_date = start_date
        while current_date <= end_date:
            query_kwargs = {
                'platformname': 'Sentinel-3',
                'instrumentshortname': 'OLCI',
                'date': (current_date, current_date + timedelta(days=1)),  # Query for a single day
                'area': wkt_bbox,  # Use the WKT representation for the bounding box, required by API
                'producttype': 'OL_1_EFR___', # Fetches EFR folders only, these are the 'best' for data analysis
                'limit': 1 # Only downloading one snapshot for the date range
            }
            pp = api.query(**query_kwargs)

            if pp:
                # If products are found on the current date, add them to the products OrderedDict and break the loop
                products.update(pp)
                break

            # Move to the next date, one day forwards, if no snapshot on current date
            current_date += timedelta(days=1)

    # Use the download_path parameter to specify the download directory
    api.download_all(products, directory_path=download_directory)

def get_olci_singular(date_tuple,     # Tuple containing start and end dates for data retrieval.
                      bbox,           # Bounding box coordinates [min_lon, min_lat, max_lon, max_lat].
                      download_directory  # Directory where downloaded data will be saved.
                      ):
    """
    Downloads a singular OLCI (Ocean and Land Color Instrument) snapshot's data based on the specified parameters.

    Args:
        date_tuple (tuple): A tuple containing the start and end dates for data retrieval.
        bbox (list): Bounding box coordinates [min_lon, min_lat, max_lon, max_lat].
        download_directory (str): The directory where downloaded data will be saved.

    Returns:
        None
    """

    wkt_bbox = mf.bbox_to_WKT(bbox)

    # Initialize an empty OrderedDict to store the products
    products = OrderedDict()

    start_date = datetime.strptime(date_tuple[0][0], '%Y-%m-%d')
    end_date = datetime.strptime(date_tuple[0][1], '%Y-%m-%d')

    # Query for products on the earliest date within the date range
    current_date = start_date
    while current_date <= end_date:
        query_kwargs = {
            'platformname': 'Sentinel-3',
            'instrumentshortname': 'OLCI',
            'date': (current_date, current_date + timedelta(days=1)),  # Query for a single day
            'area': wkt_bbox,  # Use the WKT representation for the bounding box
            'producttype': 'OL_1_EFR___',
            'limit': 1
        }
        pp = api.query(**query_kwargs)

        if pp:
            # If products are found on the current date, add them to the products OrderedDict and break the loop
            products.update(pp)
            break

        # Move to the next date
        current_date += timedelta(days=1)

    # Use the download_path parameter to specify the download directory
    api.download_all(products, directory_path=download_directory)


