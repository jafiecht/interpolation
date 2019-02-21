#This file rasterizes .shp point data

import geopandas as gpd
import rasterio
from rasterio import features
import matplotlib.pyplot as plt
import numpy as np

def rasterize(filename):

  #Filepaths
  templatefp = "./rootdata/dem.tif"
  outfp = './individuals/'

  #Read in the shapefile and add a point ID column
  data = gpd.read_file(filename)
  data['Point_ID'] = data.index
  
  #Open the template raster for template information
  template = rasterio.open(templatefp)
  meta = template.meta.copy()
  
  #Reproject the shapfile data to the raster crs
  data = data.to_crs({'init': meta['crs']['init']})
  
  #Create an individual file for each point. Useful for buffer creation.
  for index, row in data.iterrows():
    
    #Create a new raster for writing.
    with rasterio.open(outfp+str(row.Point_ID)+'.tif', 'w', **meta) as out:
      out_arr = out.read(1)
      
      #Transform and rasterize shape data
      shapes = ((geom, value) for geom, value in zip([row.geometry], [row.OM]))
      burned = features.rasterize(shapes = shapes, fill=0, out=out_arr, transform=out.transform)
      
      #Write the data out as a raster
      out.write_band(1, burned)
      out.close()
  
