import numpy as np
import rasterio
import os
#import viewer

srcfp = './individuals'
outfp = './buffers/buffer'

def make_buffers():

  files = os.listdir(srcfp)
  
  i = 0
  for filename in files:
    print(filename)
    src = srcfp + '/' + filename
    tmp = 'temp' + str(i) + '.tif'
    out = outfp + str(i) + '.tif'
  
    data = rasterio.open(src)
    meta = data.meta.copy()
    array = data.read(1)
    mask = (array != meta['nodata']).astype(np.float32)
    
    tempfile = rasterio.open(tmp, 'w', **meta)
    tempfile.write(mask, 1)
    tempfile.close()
   
    os1 = 'gdal_proximity.py ' + tmp + ' ' + out
    os.system(os1)
  
    os2 = 'rm ' + tmp
    os.system(os2)
    
    i += 1

#viewer.show_tif('./buffers/buffer109.tif')

  
