#this file imports a tif, then shows it.
import gdal
import matplotlib.pyplot as plt
from matplotlib import cm



#Load .tif file
def show_tifs():
  raster1 = gdal.Open('okpredictions.tif')
  ok = raster1.GetRasterBand(1).ReadAsArray()
  
  raster2 = gdal.Open('rfpredictions.tif')
  rf = raster2.GetRasterBand(1).ReadAsArray()

  fig = plt.figure()
      
  fig.add_subplot(1, 2, 1)
  plt.title('Ordinary Kriging')
  plt.imshow(ok, cmap = cm.Greys)
  #plt.colorbar(orientation='horizontal')
  plt.colorbar()  

  fig.add_subplot(1, 2, 2)
  plt.title('Random Forest')
  plt.imshow(rf, cmap = cm.Greys)
  #plt.colorbar(orientation='horizontal')
  plt.colorbar()  

  plt.tight_layout()  
  plt.show()
  
  raster1 = None
  raster2 = None
  return

show_tifs()
