#Tests each of the predicted files and averages the metrics

#Imports
import metrics
import os


def test(directory):
  #Get the predicted filenames
  predictlist = os.listdir(directory)

  #Define metric lists
  r2list = list()
  rmselist = list()
  melist = list()
  maelist = list()

  #Get performance metrics for each prediction
  for prediction in predictlist:
    r2, rmse, me, mae = metrics.generate_metrics(directory + prediction)
    r2list.append(r2)
    rmselist.append(rmse)
    melist.append(me)
    maelist.append(mae)

  #Calculate Average metrics
  r2 = sum(r2list)/len(r2list)
  rmse = sum(rmselist)/len(rmselist) 
  me = sum(melist)/len(melist) 
  mae = sum(maelist)/len(maelist) 
  
  print('\nR2: ', r2)
  print(r2list)
  print('\nRMSE: ', rmse)
  print(rmselist)
  print('\nMAE: ', mae)
  print(maelist)
  print('\nME: ', me)
  print(melist)

#test('krig_predictions/')
