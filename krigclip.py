#This file clips oversized kriged maps to the boundary

#Imports
import os
import shutil

#Directories
rawdir = 'raw_krig/'
outdir = 'krig_predictions/'

def clip():

  #Remove and recreate any clipped files
  shutil.rmtree(outdir)
  os.mkdir(outdir)

  #Get list of all unclipped files
  filenames = os.listdir(rawdir)

  #Clip and write for each file
  for filename in filenames:
    #Clips the raster to the boundary shapefile.
    command = 'gdalwarp -cutline rootdata/davis_boudary.shp -crop_to_cutline -dstnodata 0 ' + rawdir + filename + " " + outdir + filename[5:] 
    os.system(command)

clip()
