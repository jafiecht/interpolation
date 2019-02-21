#This file makes predictions for all the training files
#then tests each prediction.

#Imports
import predictor
import tester
import shutil
import os

#Get all training filenames
trainlist = os.listdir('train/')

#Remove existing prediction files
shutil.rmtree('rf_predictions')
os.makedirs('rf_predictions')

#Make a prediction for each train file
for train in trainlist:
  if os.path.splitext(train)[1] == '.shp':
    predictor.make_prediction('./train/' + train) 

#Get performace metrics
tester.test('rf_predictions/')

