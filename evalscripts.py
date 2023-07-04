## Aidan McEnaney
## June 30th, 2023
## Python file to store evalscripts


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