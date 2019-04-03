import geopandas as gpd
import pandas as pd
import shapely
import json
import matplotlib.pyplot as plt
import requests

def getDEM(data):
  #Load the boundary data sent from the user
  boundary = gpd.GeoDataFrame.from_features(data['features'])
  boundary.crs = {'init': 'epsg:4326'}

  #Reproject, buffer, then project back the boundary
  boundary = boundary.to_crs({'init': 'epsg:26916'})
  boundary['geometry'] = boundary['geometry'].buffer(200)
  boundary = boundary.to_crs({'init': 'epsg:4326'})

  #Import the tile extent file, then convert to a geodataframe
  extents = pd.read_csv('rootdata/randolph_boundaries.csv', sep=",", header=None, names=['path', 'geometry'])
  extents['geometry'] = extents['geometry'].apply(json.loads)
  extents['geometry'] = extents['geometry'].apply(shapely.geometry.Polygon)
  extents = gpd.GeoDataFrame(extents, geometry='geometry') 
  extents.crs = {'init': 'epsg:4326'}
  
  #Find the tiles that intersect the buffered boundary
  extents['intersects'] = extents['geometry'].intersects(boundary['geometry'][0])
  paths = extents.loc[(extents['intersects']==True)]['path'].tolist()
  
  #Read those files in
  for path in paths:
    tile = requests.get(path, allow_redirects=True)
    filename = path.rsplit('/', 1)[1]
    outfile = open('rootdata/' + filename, 'wb')
    outfile.write(tile.content)
    outfile.close()
 
