#This file handles data importing and wrangling

#Imports
###########################################################
import gdal
import numpy as np

#Script Body
###########################################################
#Sort out the labeled values from the raw dataset
def sort_dataset(raw_dataset):
  dataset = list()
  for row in raw_dataset:
    if row[-1] <= 1000:
      dataset.append(row)
  return dataset


