#This is a test file for developing the quadratic surface generator

#Imports
import rasterio
import numpy as np
import quadratic
import viewer

srcfp = './DavisClipped.tif'
outfp = './curvatures/'

raster = rasterio.open(srcfp)
elev = raster.read(1)
meta = raster.meta.copy()

resolution = meta['transform'][1]

neighborhoods = [7, 21, 49]

slfp = 0
prfp = 0
plfp = 0
tgfp = 0

for neighborhood in neighborhoods:
  print(neighborhood)
  slfp = outfp + 'slope' + str(neighborhood) + '.tif'
  prfp = outfp + 'profile' + str(neighborhood) + '.tif'
  plfp = outfp + 'plan' + str(neighborhood) + '.tif'
  tgfp = outfp + 'tang' + str(neighborhood) + '.tif'

  print(slfp)
  print(prfp)
  print(plfp)
  print(tgfp)
 
  slope, profile, plan, tangential = quadratic.slope_curvature(elev, resolution, neighborhood)

  slope_out = rasterio.open(slfp, 'w', **meta)
  slope_out.write(slope.astype(np.float32), 1)
  slope_out.close()

  profile_out = rasterio.open(prfp, 'w', **meta)
  profile_out.write(profile.astype(np.float32), 1)
  profile_out.close()

  plan_out = rasterio.open(plfp, 'w', **meta)
  plan_out.write(plan.astype(np.float32), 1)
  plan_out.close()

  tang_out = rasterio.open(tgfp, 'w', **meta)
  tang_out.write(tangential.astype(np.float32), 1)
  tang_out.close()

viewer.show_tif(slfp)
viewer.show_tif(prfp)
viewer.show_tif(plfp)
viewer.show_tif(tgfp)

