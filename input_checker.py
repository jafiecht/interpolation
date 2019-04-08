#This file validates user input and returns errors otherwise

import json
import geopandas as gpd

def check(inputObject):
  #Load Data
  boundary = gpd.GeoDataFrame.from_features(inputObject['boundary']['features'])
  boundary.crs = {'crs': 'epsg:4326'}

  points = gpd.GeoDataFrame.from_features(inputObject['points']['features'])
  points.crs = {'crs': 'epsg:4326'}
   
  write_out(boundary, points):

  
def write_out(boundary, points):
  #Reproject to UTM and write the files out
  boundary = boundary.to_crs({'init': 'epsg:26916'})
  boundary.to_file('data/rootdata/boundary.shp')

  points = points.to_crs({'init': 'epsg:26916'})
  boundary.to_file('data/rootdata/points.shp')

  
