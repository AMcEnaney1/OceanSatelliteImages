## Aidan McEnaney
## June 30th, 2023
## Python file to store evalscripts

## These evalscripts are what is used by the request functions for the SentinelHub api, requests are defined in 'requestFunctions.py'
## Information on units, bands, and sample types for the various supported satellites can be found here:
## https://docs.sentinel-hub.com/api/latest/data/
## Documentation pertaining to evalscripts in particular can be found here:
## https://docs.sentinel-hub.com/api/latest/evalscript/v3/


# Evalscript to get band 10 data in the format of 32-bit floats, these are returned in raw form, the exact satellite
# that this data is not specified here as that is specified in whatever request function calls the evalscript.
evalscript_t = """
    //VERSION=3
    function setup() {
      return {
        input: [{
          bands: ["B10"]
        }],
        output: {
          bands: 1,
          sampleType: SampleType.FLOAT32
        }
      }
    }

    function evaluatePixel(samples) {
      return [samples.B10];
    }
    """

evalscript_c = """
//VERSION=3
function setup() {
  return {
    input: [{
      bands: ["B04"]
    }],
    output: {
      bands: 1,
      sampleType: SampleType.FLOAT32
    }
  }
}

function evaluatePixel(samples) {
  return [samples.B04];
}
"""

evalscript_s = """
//VERSION=3
function setup() {
  return {
    input: [{
      bands: ["B07"]
    }],
    output: {
      bands: 1,
      sampleType: SampleType.FLOAT32
    }
  }
}

function evaluatePixel(samples) {
  return [samples.B07];
}
"""

evalscript_o = """
//VERSION=3
function setup() {
  return {
    input: [{
      bands: ["B13"]
    }],
    output: {
      bands: 1,
      sampleType: SampleType.FLOAT32
    }
  }
}

function evaluatePixel(samples) {
  return [samples.B13];
}
"""

# Evalscript to get 13 bands of data in the format of 16-bit integers, the unit type of 'DN' stands for 'digital number',
# and is the unit specified in the documentation for the SENTINEL2_L2A satellite. The satellite specified in the
# 'get_all_s2l2a_request()' function. The documentation for this is linked at the top of this file.
evalscript_all_s2l2a = """
    //VERSION=3
    function setup() {
        return {
            input: [{
                bands: ["B01","B02","B03","B04","B05","B06","B07","B08","B8A","B09","B11","B12"],
                units: "DN"
            }],
            output: {
                bands: 13,
                sampleType: "INT16"
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B01,
                sample.B02,
                sample.B03,
                sample.B04,
                sample.B05,
                sample.B06,
                sample.B07,
                sample.B08,
                sample.B8A,
                sample.B09,
                sample.B11,
                sample.B12];
    }
"""

evalscript_chlor_algo = """
    //VERSION=3
    function setup() {
        return {
            input: [{
                bands: ["B03","B04","B06","B09","B10"],
                units: "REFLECTANCE"
            }],
            output: {
                bands: 5,
                sampleType: "UINT8"
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B03,
                sample.B04,
                sample.B06,
                sample.B09,
                sample.B10];
    }
"""