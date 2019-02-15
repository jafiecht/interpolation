import rasterio
import numpy as np
import viewer

srcfp = './combined.tif'
outfp = './enriched.tif'

raster = rasterio.open(srcfp)
meta = raster.meta.copy()
array = raster.read(1)

enriched = np.full(array.shape, meta['nodata']).astype(np.float32)

for i in range(1, (array.shape[0]-1)):
  for j in range(1, (array.shape[1]-1)):
    window = array[(i-1):(i+2), (j-1):(j+2)]
    enriched[i,j] = window.min().astype(np.float32)
      

out = rasterio.open(outfp, 'w', **meta)
out.write(enriched, 1)
out.close()

viewer.show_tif(srcfp)
viewer.show_tif(outfp)


