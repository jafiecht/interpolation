#This file makes predictions for all the training files
#then tests each prediction.

#Imports
import predictor
import os

#Get all training filenames
trainlist = os.listdir('train/')

#Make a prediction for each train file
for train in trainlist:
  if os.path.splitext(train)[1] == '.shp':
    predictor.make_prediction('./train/' + train) 

