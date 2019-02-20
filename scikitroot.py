eThis is the root script of the model. Everything is called from here

#Imports
###############################################################
import import_functions
import stack
import export_functions
import viewer
from sklearn.ensemble import RandomForestRegressor

#Script Body
###############################################################
def make_prediction(filename):
  
  print(' *** Predictions will be made for ' + filename + ' *** \n')

  print(' *** Reading Inputs and Creating Feature Set *** \n')
  
  #Call in the feature set. Returns features and template data
  raw_dataset, shape, geotrans, proj = stack.return_stack(filename)

  #Sort the known rows from the dataset into a set of training data
  dataset = import_functions.sort_dataset(raw_dataset)

  #Split the datasets into feature and value sets
  raw_dataset_values = [row[-1] for row in raw_dataset]
  raw_dataset_features = [row[0:-1] for row in raw_dataset]

  dataset_values = [row[-1] for row in dataset]
  dataset_features = [row[0:-1] for row in dataset] 


  print(' *** Training Regression Forest *** \n')
  #Define the regressor parameters
  forest = RandomForestRegressor(max_depth=4, n_estimators=2000, min_samples_leaf=9)
  
  #Fit the forest to the training data
  forest.fit(dataset_features, dataset_values)
  
  print(' *** Making Predictions *** \n')
  #Feed in the raw dataset feature to predict continous values
  predictions = forest.predict(raw_dataset_features).tolist()
 
  print(' *** Writing Predictions to file *** \n')
  #Generate the output filename
  name = os.path.basename(filename)
  subname = os.path.splitext(name)[0]
  output_filename = './rf_predictions/' + 'temp' + subname + ".tif"

  #Send the predictions to file 
  export_functions.output_tif(predictions, shape, output_filename, geotrans, proj)

  print(' *** Finished *** ')
  return

#make_prediction('./train/1.shp')
