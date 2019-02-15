#This file will create validation metrics

import geopandas as gpd
import rasterio
from rasterio import features
import os

def get_pairs(predicted):
  outfp = './temp.tif'
  name = os.path.basename(predicted)
  subname = os.path.splitext(name)[0]
  testname = './test/' + subname + '.shp'  
  print(testname)
  data = gpd.read_file(testname)

  template = rasterio.open(predicted)
  predicted_array = template.read(1)
  meta = template.meta.copy()
  meta['nodata'] = 9999

  data = data.to_crs({'init': meta['crs']['init']})

  with rasterio.open(outfp, 'w', **meta) as out:
    out_arr = out.read(1)

    shapes = ((geom, value) for geom, value in zip(data.geometry, data.OM))

    burned = features.rasterize(shapes = shapes, fill=0, out=out_arr, transform=out.transform)
    out.write_band(1, burned)
    out.close()

  rasterized = rasterio.open(outfp)
  test_array = rasterized.read(1)
  
  value_pairs = list()
  for i in range(test_array.shape[0]):
    for j in range(test_array.shape[1]):
      if test_array[i, j] < 9999:
        value_pair = [test_array[i,j], predicted_array[i,j]]
        value_pairs.append(value_pair)
  
  os.system('rm ' + outfp)
  return value_pairs

def calculate_R2(y, yhat):
  ybar = sum(y)/len(y)
  n = len(y)
  SST = 0
  SSE = 0
  for i in range(n):
    ST = (y[i] - ybar)**2
    SE = (y[i] - yhat[i])**2
    SST = SST + ST
    SSE = SSE + SE
  print(1-(SSE/SST))
  R2 = 1 - SSE/SST
  return R2

def calculate_RMSE(y, yhat):
  MSE = 0
  n = len(yhat)
  for i in range(n):
    SE = (yhat[i] - y[i])**2
    MSE = MSE + SE
  RMSE = (MSE/n)**(1/2)
  return RMSE

def calculate_ME(y, yhat):
  ME = 0
  n = len(yhat)
  for i in range(n):
    E = (yhat[i] - y[i])
    ME = ME + E
  ME = (ME/n)
  return ME

def generate_metrics(predicted): 
  values = get_pairs(predicted)
  y = [row[0] for row in values]
  yhat = [row[1] for row in values]
  r2 = calculate_R2(y, yhat)
  rmse = calculate_RMSE(y, yhat)
  me = calculate_ME(y, yhat)
  print('R2 Score: ' + str(r2))  
  print('RMSE: ' + str(rmse))  
  print('ME: ' + str(me))  
  return r2, rmse, me

generate_metrics('./rf_predictions/1.tif')
