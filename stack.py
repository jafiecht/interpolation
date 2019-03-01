#This file reads all our feature sets and assembles 
#a feature set.

#Imports
import rasterio
import gdal
import numpy as np
import os
import shutil
import rasterizer
import buffers
import recombine
import enricher

#Filepaths
elevfp = 'rootdata/dem.tif'
flowaccfp = 'topo_features/FlowAcc.tif'
hordistfp = 'topo_features/hor_dist.tif'
twifp = 'topo_features/normalized_twi.tif'
slopefp = 'topo_features/slope.tif'
curvdir = 'topo_features/curvatures/'
bufferdir = 'buffers/'
valuesfp = 'combined.tif'
enrichedfp = 'enriched.tif'

def return_stack(filename):
  #ex: ./train/1.shp
  
  #Define stack
  arrays = list()
  labels = list()

  #Import Elevation
  ##########################
  elev_raster = rasterio.open(elevfp)
  elev = elev_raster.read(1)
  arrays.append(elev)
  labels.append('Elevation')

  #Import Flow Accumulation (jk, apparently it's worthless)
  ##########################
  #flow_raster = rasterio.open(flowaccfp)
  #flow = flow_raster.read(1)
  #arrays.append(flow)
  #labels.append('Flow Accumulation')

  #Import Horizontal Distance (worthless. Odd.)
  ##########################
  #hordist_raster = rasterio.open(hordistfp)
  #hordist = hordist_raster.read(1)
  #arrays.append(hordist)
  #labels.append('Horizontal Distance')

  #Import twi (apparently, also worthless)
  ##########################
  #twi_raster = rasterio.open(twifp)
  #twi = twi_raster.read(1)
  #arrays.append(twi)
  #labels.append('TWI')

  #Import slope
  ##########################
  slope_raster = rasterio.open(slopefp)
  slope = slope_raster.read(1)
  arrays.append(slope)
  labels.append('Local Slope')

  #Import Multi-Neighborhood curvatures
  ##########################
  curvlist = os.listdir(curvdir)
  for instance in curvlist:
    curve_raster = rasterio.open(curvdir + instance)
    curve = curve_raster.read(1)
    arrays.append(curve)
    labels.append(os.path.splitext(instance)[0])

  #Rasterize input shapefile
  ##########################
  #Delete any files currently in the individuals folder
  shutil.rmtree('individuals')
  os.makedirs('individuals')
  rasterizer.rasterize(filename)

  #Create Euclidean Distances
  ##########################
  #Delete any files currently in the individuals folder
  shutil.rmtree('buffers')
  os.makedirs('buffers')
  buffers.make_buffers()

  #Import Buffer Distances
  ##########################
  bufferlist = os.listdir(bufferdir)
  for instance in bufferlist:
    buffer_raster = rasterio.open(bufferdir + instance)
    buffer_array = buffer_raster.read(1)
    arrays.append(buffer_array)
    labels.append('buffer ' + os.path.splitext(instance)[0])

  #Create combined point raster
  ##########################
  #Delete any previous combined raster
  if os.path.isfile(valuesfp): 
    os.remove(valuesfp)
  recombine.recombine()
  if os.path.isfile(enrichedfp): 
    os.remove(enrichedfp)
  enricher.enrich()

  #Import Training Values
  ##########################
  values_raster = rasterio.open(valuesfp)
  values = values_raster.read(1)
  arrays.append(values)
  
  #Transform feature arrays into 1-d lists
  ##########################
  raster_shape = arrays[0].shape
  stack = np.zeros(shape=((raster_shape[0]*raster_shape[1]), len(arrays)))
  index = 0
  #Loop through all 3 dimensions
  for i in range(raster_shape[0]):
    for j in range(raster_shape[1]):
      for array_index in range(len(arrays)):
        #Assign values to the 2-d stack from the 3-d array set
        stack[index, array_index] = arrays[array_index][i,j]
      index += 1

  #Get template data
  ##########################
  raster = gdal.Open(elevfp)
  geotrans = raster.GetGeoTransform()
  proj = raster.GetProjection()

  #print(arrays)
  #print(labels)
  return stack.tolist(), raster_shape, geotrans, proj, labels

  
#testStack, shape, geotransformation, projection = return_stack('./train/1.shp')

#print(testStack)

  
