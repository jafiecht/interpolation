#Inspects all the rf predicted maps

#Imports
import os
import viewer

#Get list of all predictions
filenames = os.listdir('rf_predictions')

#View every file
for filename in filenames:
  viewer.show_tif('rf_predictions/' + filename)

