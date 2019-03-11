#This file makes predictions for all the training files
#then tests each prediction.

#Imports
import rasterizer
import buffers
import recombine
import stack
import predictor
import export_functions
import metrics
import tester
import shutil
import os

def cross_validation(filename):

  #Remove existing individual points
  #shutil.rmtree('individuals')
  #os.makedirs('individuals')

  #Rasterize the shapefile
  #rasterizer.rasterize(filename)

  #Remove existing buffer layers
  #shutil.rmtree('buffers')
  #os.makedirs('buffers') 

  #Create buffer layers for each point
  #buffers.make_buffers()

  #Get the filename of all individual points
  points = os.listdir('individuals')

  #Define y and yhat list
  value_pairs = list()

  #Run the function for each filename
  for point in points:
    print(point)    

    #Take the validation point out of the training set
    training = points.copy()
    training.remove(point)
   
    #Create a recombined raster, removing old raster
    if os.path.isfile('combined.tif'):
      os.remove('combined.tif')
    recombine.recombine(training)

    #Create the stack
    raw_dataset, raster_shape, geotrans, proj, labels = stack.return_stack(training)
  
    #Generate Prediction
    #Possible Performance hack: only predict the validation point, not the whole raster
    predictions = predictor.make_prediction(raw_dataset) 
    
    #Create prediction output name
    output_filename = 'cv' + point
   
    #Write Prediction out
    export_functions.output_tif(predictions, raster_shape, geotrans, proj, output_filename)

    #Get y and yhat pair, append to list
    pairs = metrics.get_pairs(point, output_filename)
    value_pairs = value_pairs + pairs

  print(value_pairs)

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
