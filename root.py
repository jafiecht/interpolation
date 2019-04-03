#This file makes predictions for all the training files
#then tests each prediction.

#Imports
import tile_selector
import rasterizer
import buffers
import stack
import predictor
import export_functions
import metrics
import tester
import viewer
import numpy as np
import shutil
import os
import json

def validate_predict(inputObject):
  #Select raster tiles with field boundary
  tile_selector.getDEM(inputObject['boundary'])

  ##Remove existing individual points and recreate
  #shutil.rmtree('individuals')
  #os.makedirs('individuals')
  #rasterizer.rasterize(filename)
  #point_data = stack.return_points()

  ##Remove existing buffer layers and recreate
  #shutil.rmtree('buffers')
  #os.makedirs('buffers') 
  #buffers.make_buffers()
  #buffers = stack.return_buffers()

  #Retrieve topographic layers
  #topo = stack.return_topo()

  #Get predictions
  #scores = validate(point_data, topo, buffers)

  #Make master prediction
  #predictions = map_predictions(point_data, topo, buffers)

  #Get Template Data and write data out
  #raster_shape, geotrans, proj = stack.template(topo)
  #export_functions.output_tif(predictions, raster_shape, geotrans, proj, 'rfpredictions.tif')
  
  #viewer.show_tif('rfpredictions.tif')
  return

#This performs an n-fold cross validation test
def validate(point_data, topo, buffers):
  #Run the function for each filename
  points = list(point_data.keys())
  value_pairs = list()
  iteration = 0
  length = len(points)
  for test_point in points: 

    #Take the validation point out of the training set
    training_points = points.copy()
    training_points.remove(test_point)
    training_buffers = training_points
 
    #Assemble the training set
    training_set = list()
    for training_point in training_points:
      obs = list()
      for feature in topo:
        obs.append(feature[point_data[training_point]['index']])
      for buffer_feature in training_buffers:
        obs.append(buffers[buffer_feature][point_data[training_point]['index']])
      obs.append(point_data[training_point]['value'])
      training_set.append(obs)

    #Assemble the test set
    testing_set = list()
    obs = list()
    for feature in topo:
      obs.append(feature[point_data[test_point]['index']])
    for buffer_feature in training_buffers:
      obs.append(buffers[buffer_feature][point_data[test_point]['index']])
    testing_set.append(obs)

    #Generate Prediction
    prediction = predictor.train_predict(training_set, testing_set) 
    
    value_pairs.append([point_data[test_point]['value'], prediction[0]])
        
    #Log Progress
    iteration += 1
    print(str(int(iteration/length*90)+5)+'%')

  scores = metrics.generate_metrics(value_pairs)

  print('R2 Score: ' + str(scores[0]))  
  print('RMSE: ' + str(scores[1]))  
  print('ME: ' + str(scores[2]))  
  print('MAE: ' + str(scores[3]))  
  return scores
  

def map_predictions(point_data, topo, buffers):
  
  #Define iterables
  points = list(point_data.keys())
  training_buffers = points
  
  #Assemble the training set
  training_set = list()
  for training_point in points:
    obs = list()
    for feature in topo:
      obs.append(feature[point_data[training_point]['index']])
    for buffer_feature in training_buffers:
      obs.append(buffers[buffer_feature][point_data[training_point]['index']])
    obs.append(point_data[training_point]['value'])
    training_set.append(obs)
  
  #Assemble the prediction set
  feature_set = topo.copy()
  for buffer_feature in training_buffers:
    feature_set.append(buffers[buffer_feature])

  #Transform feature_set into 1-d lists
  raster_shape = feature_set[0].shape
  stack = np.zeros(shape=((raster_shape[0]*raster_shape[1]), len(feature_set)))
  index = 0
  #Loop through all 3 dimensions
  for i in range(raster_shape[0]):
    for j in range(raster_shape[1]):
      for feature_index in range(len(feature_set)):
        #Assign values to the 2-d stack from the 3-d array set
        stack[index, feature_index] = feature_set[feature_index][i,j]
      index += 1

  #Generate Predictions
  predictions = predictor.train_predict(training_set, stack.tolist()) 
  return predictions    


#validate_predict('rootdata/combined_soil.shp')
