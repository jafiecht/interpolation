#Inspects all the rf predicted maps

#Imports
import os
import viewer

#Get list of all predictions
filenames = os.listdir('krig_predictions')

#View every file
for filename in filenames:
  viewer.show_tif('krig_predictions/' + filename)

