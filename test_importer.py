import geopandas as gpd
import rasterio
from rasterio import features
import matplotlib.pyplot as plt
import numpy as np
#import viewer


def rasterize(filename):
  templatefp = "./DavisClipped.tif"
  outfp = './individuals/point'

  data = gpd.read_file(filename)
  data['Point_ID'] = data.index
  
  
  template = rasterio.open(templatefp)
  meta = template.meta.copy()
  
  data = data.to_crs({'init': meta['crs']['init']})
  
  for index, row in data.iterrows():
    with rasterio.open(outfp+str(row.Point_ID)+'.tif', 'w', **meta) as out:
      out_arr = out.read(1)
  
      shapes = ((geom, value) for geom, value in zip([row.geometry], [row.OM]))
      
      burned = features.rasterize(shapes = shapes, fill=0, out=out_arr, transform=out.transform)
      out.write_band(1, burned)
      out.close()
  
  #viewer.show_tif(templatefp)
  #viewer.show_tif(outfp + '109.tif')
  
  #data.plot()
  #plt.show()
