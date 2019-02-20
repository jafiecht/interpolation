#This is a test file for developing the quadratic surface generator

#Imports
import rasterio
import numpy as np
import quadratic
import viewer

#The filepaths for the input DEM and output directories
srcfp = './DavisClipped.tif'
outfp = './curvatures/'

#Open the Raster and Extract needed data
raster = rasterio.open(srcfp)
elev = raster.read(1)
meta = raster.meta.copy()
resolution = meta['transform'][1]

#Set the neighborhoods to generate for
neighborhoods = [7, 21, 49]

#For every neighborhood size, loop through and create maps
for neighborhood in neighborhoods:

  #Create output filepaths
  slfp = outfp + 'slope' + str(neighborhood) + '.tif'
  prfp = outfp + 'profile' + str(neighborhood) + '.tif'
  plfp = outfp + 'plan' + str(neighborhood) + '.tif'
  tgfp = outfp + 'tang' + str(neighborhood) + '.tif'

  #Call the slope generation function, returns arrays 
  slope, profile, plan, tangential = quadratic.slope_curvature(elev, resolution, neighborhood)

  #Write out the arrays as tifs
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
