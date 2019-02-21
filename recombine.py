#This file combines all the individual raster point files
#into one file.

#Imports
import rasterio
import numpy as np
import os

#Filepaths
srcfp = './individuals/'
template = './rootdata/dem.tif'
outfp = 'combined.tif'


def recombine():

  #Opena and use the main dem as a template
  template_raster = rasterio.open(template)
  template_meta = template_raster.meta.copy()
  template_array = template_raster.read(1)
  
  #Initialize a combined array using the template shape and nodata
  combined = np.full(template_array.shape, template_meta['nodata']).astype(np.float32)
 
  #Get a list of all the individual raster files
  files = os.listdir(srcfp)
   
  #Execute for all individual rasters
  for filename in files:
   
    #Open the input raster
    src = srcfp + filename
    data = rasterio.open(src)
    meta = data.meta.copy()
    array = data.read(1)
  
    #Get the 1-d location of the min value (the real datapoint)
    flat_index = np.argmin(array)

    #Transform the 1-d index into a 2-d index
    index = np.unravel_index(flat_index, array.shape)

    #Write the value into the combined array
    combined[index[0], index[1]] = array[index[0], index[1]]

    #Close the input raster
    data.close()
  
  #Write the combined array to file
  out = rasterio.open(outfp, 'w', **meta)
  out.write(combined, 1)
  out.close()


