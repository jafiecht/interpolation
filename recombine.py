import rasterio
import numpy as np
import os
#import viewer

srcfp = './individuals'
template = 'DavisClipped.tif'
outfp = 'combined.tif'

def recombine():

  template_raster = rasterio.open(template)
  template_meta = template_raster.meta.copy()
  template_array = template_raster.read(1)
  
  combined = np.full(template_array.shape, template_meta['nodata']).astype(np.float32)
 
  files = os.listdir(srcfp)
   
  for filename in files:
    src = srcfp + '/' + filename
    data = rasterio.open(src)
    meta = data.meta.copy()
    array = data.read(1)
    flat_index = np.argmin(array)
    index = np.unravel_index(flat_index, array.shape)
    combined[index[0], index[1]] = array[index[0], index[1]]
    data.close()
  
  out = rasterio.open(outfp, 'w', **meta)
  out.write(combined, 1)
  out.close()

#viewer.show_tif(outfp)

