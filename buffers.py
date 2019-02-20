#This file takes in rasterized points and creates
#euclidean distance maps.

#Imports
import numpy as np
import rasterio
import os

#Filepaths to the input points and output files
srcfp = './individuals'
outfp = './buffers/buffer'

#The function that creates the distance maps
def make_buffers():

  #This lists all the rasterized point files
  files = os.listdir(srcfp)
  
  #Execute this function for every input file
  i = 0
  for filename in files:
    
    #Generate filepaths
    src = srcfp + '/' + filename
    tmp = 'temp' + str(i) + '.tif'
    out = outfp + str(i) + '.tif'
  
    #Open the input file, read data and metadata
    data = rasterio.open(src)
    meta = data.meta.copy()
    array = data.read(1)
    
    #Create a boolean array of nodata and data points
    #This is what the proximity tool requires
    mask = (array != meta['nodata']).astype(np.float32)
    
    #Write the boolean array out as a temp file
    tempfile = rasterio.open(tmp, 'w', **meta)
    tempfile.write(mask, 1)
    tempfile.close()
   
    #This gdal command creates euclidean distance maps
    os1 = 'gdal_proximity.py ' + tmp + ' ' + out
    os.system(os1)
  
    #Remove the temp file
    os2 = 'rm ' + tmp
    os.system(os2)
    
    #Increment the index
    i += 1

