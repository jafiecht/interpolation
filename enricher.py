#This file assigns the min (real) value of a 3x3
#window to the output file. Useful for data enriching

#Imports
import rasterio
import numpy as np

#Filepaths
srcfp = './combined.tif'
outfp = './enriched.tif'

def enrich():
  #Read in the input raster
  raster = rasterio.open(srcfp)
  meta = raster.meta.copy()
  array = raster.read(1)
  
  #Define the output array with the same characteristics
  enriched = np.full(array.shape, meta['nodata']).astype(np.float32)
  
  #Sliding window operation. Assign min (real) value.
  for i in range(1, (array.shape[0]-1)):
    for j in range(1, (array.shape[1]-1)):
      window = array[(i-1):(i+2), (j-1):(j+2)]
      enriched[i,j] = window.min().astype(np.float32)
        
  #Write out the output array with the same metadata
  out = rasterio.open(outfp, 'w', **meta)
  out.write(enriched, 1)
  out.close()

