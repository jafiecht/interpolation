#This file rasterizes .shp point data

import geopandas as gpd
import rasterio
from rasterio import features
import matplotlib.pyplot as plt
import numpy as np

def rasterize(data):

  #Filepaths
  templatefp = "./rootdata/topo/elev.tif"
  outfp = '.data/individuals/'

  #Make a geodataframe, reproject to utm, then create an ID column
  points = gpd.GeoDataFrame.from_features(data['features'])
  points.crs = {'init': 'epsg:4326'}
  points = points.to_crs({'init': 'epsg:26916'})
  points['Point_ID'] = points.index

  print(points)
  
#  #Open the template raster for template information
#  template = rasterio.open(templatefp)
#  meta = template.meta.copy()
#  
#  #Create an individual file for each point. Useful for buffer creation.
#  for index, row in points.iterrows():
#    
#    #Create a new raster for writing.
#    with rasterio.open(outfp+str(row.Point_ID)+'.tif', 'w', **meta) as out:
#      out_arr = out.read(1)
#      
#      #Transform and rasterize shape data
#      shapes = ((geom, value) for geom, value in zip([row.geometry], [row.OM]))
#      burned = features.rasterize(shapes = shapes, fill=0, out=out_arr, transform=out.transform)
#      
#      #Write the data out as a raster
#      out.write_band(1, burned)
#      out.close()
  
