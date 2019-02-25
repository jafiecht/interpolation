#Inspects all the rf predicted maps

#Imports
import os
import viewer

def check(directory):
  
  #Get list of all predictions
  filenames = os.listdir(directory)

  #View every file
  for filename in filenames:
    viewer.show_tif(directory + filename)

