#This file reads all our feature sets and assembles 
#a feature set.

#Imports
import rasterio
import gdal
import numpy as np
import os
#import shutil
import rasterizer
import buffers
import recombine
import enricher

#Filepaths
elevfp = 'rootdata/dem.tif'
#flowaccfp = 'topo_features/FlowAcc.tif'
#hordistfp = 'topo_features/hor_dist.tif'
#twifp = 'topo_features/normalized_twi.tif'
slopefp = 'topo_features/slope.tif'
curvdir = 'topo_features/curvatures/'


#This function returns a dict. with point values and location
def return_points():
  #Get all the files to run
  filenames = os.listdir('individuals')

  #Run for each file
  point_data = {}  
  for filename in filenames:
    #Open the input raster
    raster = rasterio.open('individuals/' + filename)
    array = raster.read(1)

    #Get the index for the min value (the datapoint)
    flat_index = np.argmin(array)
    index = np.unravel_index(flat_index, array.shape)
    
    #Write the data to the dictionary
    key = os.path.splitext(filename)[0]
    point_data[key] = {'index': index, 'value': array[index]}

  return point_data


#This function returns a dict. with buffer arrays
def return_buffers():
  #Get all the files to run
  filenames = os.listdir('buffers')

  #Run for each file
  buffers = {}  
  for filename in filenames:
    #Open the input raster
    raster = rasterio.open('buffers/' + filename)
    array = raster.read(1)
    
    #Write the data to the dictionary
    key = os.path.splitext(filename)[0]
    buffers[key] = array

  return buffers


def return_topo():
  
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

  return arrays #, labels


def template(feature_set):

  #Get template data
  raster_shape = feature_set[0].shape
  raster = gdal.Open(elevfp)
  geotrans = raster.GetGeoTransform()
  proj = raster.GetProjection()

  return raster_shape, geotrans, proj

