#this file imports a tif, then shows it.
import gdal
import matplotlib.pyplot as plt
from matplotlib import cm



#Load .tif file
def show_tif(filename):
  print(filename)
  raster = gdal.Open(filename)
  for i in range(raster.RasterCount):
    i += 1
    #print('Band'+str(i))
    band = raster.GetRasterBand(i).ReadAsArray()
    if (i < 12):
      plt.imshow(band, cmap = cm.Greys)
      plt.colorbar()
      plt.show()
  raster = None
  return


