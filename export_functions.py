#Imports
###########################################################
import gdal
import numpy as np
import os
import viewer

#Script Body
###########################################################
#Create output filenames from input filename
def generate_filenames(filename):
  name = os.path.basename(filename)
  subname = os.path.splitext(name)[0]
  filename1 = './rf_predictions/' + 'temp' + subname + ".tif" 
  #filename2 = content + '_stdev.tif'
  return filename1

#Transform prediction list into output tif
def output_tif(predictions, shape, filename, geotrans, proj):
  prediction_list = predictions
  prediction_array = list()
  for i in range(shape[0]):
    prediction_array.append(prediction_list[0:(shape[1])])
    for j in range(shape[1]):
      if len(prediction_list) > 0:
        prediction_list.pop(0)
  band = np.array(prediction_array)
  x_pixels = shape[1]
  y_pixels = shape[0]
  driver = gdal.GetDriverByName('GTiff')
  dataset = driver.Create(filename, x_pixels, y_pixels, 1, gdal.GDT_Float32)
  dataset.GetRasterBand(1).WriteArray(band)
  dataset.SetGeoTransform(geotrans)
  dataset.SetProjection(proj)
  dataset.FlushCache()
  dataset = None
  clip(filename)
  return

#Clip to field boundary
def clip(filename):
  name = os.path.basename(filename)
  shortname = name[4:]
  outpath = './rf_predictions/' + shortname

  command = 'gdalwarp -cutline davis_boudary.shp -crop_to_cutline ' + filename + " " + outpath
  os.system(command)
  os.system('rm ' + filename)
  viewer.show_tif(outpath)

