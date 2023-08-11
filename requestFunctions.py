## Aidan McEnaney
## June 30th, 2023
## Python file to store requests for sentinelHub API

## Start of imports

import evalscripts
from sentinelhub import (
    DataCollection,
    MimeType,
    MosaickingOrder,
    SentinelHubRequest,
)

## End of imports

## These are the request functions used by the SentinelHub api, they utilize the evalscripts in 'evalscripts.py'
## Information on units, bands, and sample types for the various supported satellites can be found here:
## https://docs.sentinel-hub.com/api/latest/data/
## Documentation for sentinelHub requests is scattered across the previous page and this one:
## https://docs.sentinel-hub.com/api/latest/evalscript/v3/


# This is the request for thermal data, using the evalscript 'evalscript_t'. We declare that we are using this
# evalscript and what satellite we are using here. This is also where the output response type is defined
# as well as the mosaicking order, information on the supported mosaicking orders for a specific satellite can
# be found on the individual satellite's page on the first website linked above.
def get_thermal_request(time_interval, farm_bbox, farm_size, config):
    """
    Generate a SentinelHubRequest for thermal data using the provided parameters.

    Args:
        time_interval (tuple): Start and end date of the data acquisition interval.
        farm_bbox (BoundingBox): Bounding box defining the area of interest.
        farm_size (tuple): Width and height of the output image in pixels.
        config (SHConfig): Configuration settings for the request.

    Returns:
        SentinelHubRequest: The generated SentinelHubRequest object.
    """

    return SentinelHubRequest(
        evalscript=evalscripts.evalscript_t,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.LANDSAT_OT_L2,
                time_interval=time_interval,
                mosaicking_order=MosaickingOrder.LEAST_CC,
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=farm_bbox,
        size=farm_size,
        config=config,
    )

def get_chlorophyll_request(time_interval, farm_bbox, farm_size, config):
    """
    Generate a SentinelHubRequest for chlorophyll data using the provided parameters.

    Args:
        time_interval (tuple): Start and end date of the data acquisition interval.
        farm_bbox (BoundingBox): Bounding box defining the area of interest.
        farm_size (tuple): Width and height of the output image in pixels.
        config (SHConfig): Configuration settings for the request.

    Returns:
        SentinelHubRequest: The generated SentinelHubRequest object.
    """

    return SentinelHubRequest(
        evalscript=evalscripts.evalscript_c,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL3_OLCI,
                time_interval=time_interval,
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=farm_bbox,
        size=farm_size,
        config=config,
    )

def get_sediment_request(time_interval, farm_bbox, farm_size, config):
    """
    Generate a SentinelHubRequest for sediment data using the provided parameters.

    Args:
        time_interval (tuple): Start and end date of the data acquisition interval.
        farm_bbox (BoundingBox): Bounding box defining the area of interest.
        farm_size (tuple): Width and height of the output image in pixels.
        config (SHConfig): Configuration settings for the request.

    Returns:
        SentinelHubRequest: The generated SentinelHubRequest object.
    """

    return SentinelHubRequest(
        evalscript=evalscripts.evalscript_s,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL3_OLCI,
                time_interval=time_interval,
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=farm_bbox,
        size=farm_size,
        config=config,
    )

def get_oxygen_request(time_interval, farm_bbox, farm_size, config):
    """
    Generate a SentinelHubRequest for oxygen data using the provided parameters.

    Args:
        time_interval (tuple): Start and end date of the data acquisition interval.
        farm_bbox (BoundingBox): Bounding box defining the area of interest.
        farm_size (tuple): Width and height of the output image in pixels.
        config (SHConfig): Configuration settings for the request.

    Returns:
        SentinelHubRequest: The generated SentinelHubRequest object.
    """

    return SentinelHubRequest(
        evalscript=evalscripts.evalscript_o,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL3_OLCI,
                time_interval=time_interval,
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=farm_bbox,
        size=farm_size,
        config=config,
    )

# This is a bulk request, there is really no difference, in the definition at least, between singular and bulk requests.
# The only difference is how the output is handled as the request now returns a different shape of array.
def get_all_s2l2a_request(time_interval, farm_bbox, farm_size, config):
    """
    Generate a bulk SentinelHubRequest for Sentinel-2 L2A data using the provided parameters.

    Args:
        time_interval (tuple): Start and end date of the data acquisition interval.
        farm_bbox (BoundingBox): Bounding box defining the area of interest.
        farm_size (tuple): Width and height of the output image in pixels.
        config (SHConfig): Configuration settings for the request.

    Returns:
        SentinelHubRequest: The generated SentinelHubRequest object.
    """

    return SentinelHubRequest(
        evalscript=evalscripts.evalscript_all_s2l2a,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L2A,
                time_interval=time_interval,
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=farm_bbox,
        size=farm_size,
        config=config,
)

def get_chlor_algo_request(time_interval, farm_bbox, farm_size, config):
    """
    Generate a SentinelHubRequest for chlorophyll algorithm data using the provided parameters.

    Args:
        time_interval (tuple): Start and end date of the data acquisition interval.
        farm_bbox (BoundingBox): Bounding box defining the area of interest.
        farm_size (tuple): Width and height of the output image in pixels.
        config (SHConfig): Configuration settings for the request.

    Returns:
        SentinelHubRequest: The generated SentinelHubRequest object.
    """

    return SentinelHubRequest(
        evalscript=evalscripts.evalscript_chlor_algo,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL3_OLCI,
                time_interval=time_interval,
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=farm_bbox,
        size=farm_size,
        config=config,
)