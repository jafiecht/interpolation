#This file makes predictions for all the training files
#then tests each prediction.

#Imports
import rasterizer
import buffers
import stack
import predictor
import export_functions
import metrics
import tester
import shutil
import os

def cross_validation(filename):

  ##Remove existing individual points and recreate
  #shutil.rmtree('individuals')
  #os.makedirs('individuals')
  #rasterizer.rasterize(filename)
  point_data = stack.return_points()

  ##Remove existing buffer layers and recreate
  #shutil.rmtree('buffers')
  #os.makedirs('buffers') 
  #buffers.make_buffers()
  buffers = stack.return_buffers()

  #Retrieve topographic layers
  topo = stack.return_topo()
 
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

  r2, rmse, me, mae = metrics.generate_metrics(value_pairs)

  print('R2 Score: ' + str(r2))  
  print('RMSE: ' + str(rmse))  
  print('ME: ' + str(me))  
  print('MAE: ' + str(mae))  

  

#    #Create prediction output name
#    output_filename = 'cv' + point
#   
#    #Write Prediction out
#    export_functions.output_tif(predictions, raster_shape, geotrans, proj, output_filename)
#
#    #Get y and yhat pair, append to list
#    pairs = metrics.get_pairs(point, output_filename)
#    value_pairs = value_pairs + pairs

  #print(value_pairs)

#Get all training filenames
#trainlist = os.listdir('train/')



#Remove existing prediction files
#shutil.rmtree('rf_predictions')
#os.makedirs('rf_predictions')

#Make a prediction for each train file
#for train in trainlist:
  #if os.path.splitext(train)[1] == '.shp':
    #predictor.make_prediction('./train/' + train) 

#Get performace metrics
#tester.test('rf_predictions/')

cross_validation('rootdata/combined_soil.shp')
