## Aidan McEnaney
## August 1st, 2023
## Python file to store requests for sentinelsat API

## Start of imports

from datetime import datetime, timedelta
from collections import OrderedDict
import satFunctions
from configg import *

## End of imports

def get_olci(date_tuples, bbox, download_directory):
    wkt_bbox = satFunctions.bbox_to_WKT(bbox)

    # Initialize an empty OrderedDict to store the products
    products = OrderedDict()

    for i in range(len(date_tuples)):
        start_date = datetime.strptime(date_tuples[i][0], '%Y-%m-%d')
        end_date = datetime.strptime(date_tuples[i][1], '%Y-%m-%d')

        # Initialize an empty OrderedDict to store the products
        #products = OrderedDict()

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

def get_olci_singlular(date_tuple, bbox, download_directory):
    wkt_bbox = satFunctions.bbox_to_WKT(bbox)

    # Initialize an empty OrderedDict to store the products
    products = OrderedDict()

    start_date = datetime.strptime(date_tuple[0][0], '%Y-%m-%d')
    end_date = datetime.strptime(date_tuple[0][1], '%Y-%m-%d')

    # Initialize an empty OrderedDict to store the products
    #products = OrderedDict()

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


