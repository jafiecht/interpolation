import geopandas as gpd
import pandas as pd
import shapely
import json
import matplotlib.pyplot as plt
import requests
import subprocess
import os

def getDEM(data):
  #Load the boundary data sent from the user
  #################################################################
  boundary = gpd.GeoDataFrame.from_features(data['features'])
  boundary.crs = {'init': 'epsg:4326'}

  #Reproject, buffer, then project back the boundary
  #################################################################
  boundary = boundary.to_crs({'init': 'epsg:26916'})
  boundary.to_file('data/rootdata/boundary.shp')
  buffered = boundary.copy()
  buffered['geometry'] = buffered['geometry'].buffer(200)
  buffered.to_file('data/rootdata/buffered_boundary.shp')
  buffered = buffered.to_crs({'init': 'epsg:4326'})

  #Import the tile extent file, then convert to a geodataframe
  #################################################################
  extents = pd.read_csv('data/rootdata/boundaries.csv', sep=",", header=None, names=['path', 'geometry'])
  extents['geometry'] = extents['geometry'].apply(json.loads)
  extents['geometry'] = extents['geometry'].apply(shapely.geometry.Polygon)
  extents = gpd.GeoDataFrame(extents, geometry='geometry') 
  extents.crs = {'init': 'epsg:4326'}
  
  #Find the tiles that intersect the buffered boundary
  #################################################################
  extents['intersects'] = extents['geometry'].intersects(buffered['geometry'][0])
  paths = extents.loc[(extents['intersects']==True)]['path'].tolist()
  
  #Read those files in
  #################################################################
  filenames = list()
  for path in paths:
    tile = requests.get(path, allow_redirects=True)
    filename = path.rsplit('/', 1)[1]
    filenames.append('data/rootdata/' + filename)
    outfile = open('data/rootdata/' + filename, 'wb')
    outfile.write(tile.content)
    outfile.close()

  #Process the downloaded tiles
  #################################################################
  #Merge the tiles, then remove them
  if os.path.isfile('data/rootdata/merged.tif'):
    subprocess.call('rm data/rootdata/merged.tif', shell=True)
  command = 'gdal_merge.py -o data/rootdata/merged.tif -of GTiff'
  for filename in filenames:
    command = command + ' ' + filename
  subprocess.call(command, shell=True)
  for filename in filenames:
    subprocess.call('rm ' + filename, shell=True)

  #Convert to UTM 16 and remove the merged file
  if os.path.isfile('data/rootdata/utm.tif'):
    subprocess.call('rm data/rootdata/utm.tif', shell=True)
  subprocess.call('gdalwarp -t_srs EPSG:26916 data/rootdata/merged.tif data/rootdata/utm.tif', shell=True)
  subprocess.call('rm data/rootdata/merged.tif', shell=True)

  #Clip the raster to the buffered boundary and remove the unclipped raster
  if os.path.isfile('data/rootdata/elev.tif'):
    subprocess.call('rm data/rootdata/elev.tif', shell=True)
  subprocess.call('gdalwarp -cutline data/rootdata/buffered_boundary.shp -crop_to_cutline data/rootdata/utm.tif data/rootdata/elev.tif', shell=True)
  subprocess.call('rm data/rootdata/utm.tif', shell=True)

  



