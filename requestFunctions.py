## Aidan McEnaney
## June 30th, 2023
## Python file to store requests


## Imports

import satFunctions
import evalscripts
import keys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io
import datetime
import os
from sentinelhub import (
    CRS,
    BBox,
    DataCollection,
    DownloadRequest,
    MimeType,
    MosaickingOrder,
    SentinelHubDownloadClient,
    SentinelHubRequest,
    bbox_to_dimensions,
    SHConfig,
)
from utils import plot_image
import math

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