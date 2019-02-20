#This file handles data importing and wrangling

#Imports
###########################################################
import gdal
import numpy as np

#Script Body
###########################################################
#Load .tif file
def load_tif(filename):

  #Read in input data, create list of bands
  raster = gdal.Open(filename)
  geotrans = raster.GetGeoTransform()
  proj = raster.GetProjection()
  bands = list()
  for i in range(raster.RasterCount):
    i += 1
    band = raster.GetRasterBand(i).ReadAsArray()
    bands.append(band)
  raster_shape = bands[0].shape
  dataset = np.zeros(shape=((raster_shape[0]*raster_shape[1]), len(bands)))
  index = 0
  
  #Transform bands arrays into lists
  for i in range(raster_shape[0]):
    for j in range(raster_shape[1]):
      for band_index in range(len(bands)):
        dataset[index, band_index] = bands[band_index][i,j]
      index += 1
  return dataset.tolist(), raster_shape, geotrans, proj

#Sort out the labeled values from the raw dataset
def sort_dataset(raw_dataset):
  dataset = list()
  for row in raw_dataset:
    if row[-1] <= 1000:
      dataset.append(row)
  return dataset


