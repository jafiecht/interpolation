#This file reads all our feature sets and assembles 
#a feature set.

#Imports
import rasterio
import rasterizer

#Filepaths



def return_stack(filename):
  #ex: ./train/1.shp
  
  #Import Elevation
  ##########################
  

  #Rasterize shapefile
  ##########################
  #Delete any files currently in the individual folder
  os.system('rm ./individuals/*')
  rasterizer.rasterize(filename)
  

  
