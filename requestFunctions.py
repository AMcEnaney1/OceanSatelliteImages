## Aidan McEnaney
## June 30th, 2023
## Python file to store requests


## Imports

import evalscripts
from sentinelhub import (
    DataCollection,
    MimeType,
    MosaickingOrder,
    SentinelHubRequest,
)

## End of Imports

def get_thermal_request(time_interval, farm_bbox, farm_size, config):
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

def get_all_s2l2a_request(time_interval, farm_bbox, farm_size, config):
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