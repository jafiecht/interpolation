#This is the root script of the model. Everything is called from here

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

  print(' *** Reading Input File *** \n')
  raw_dataset, shape, geotrans, proj = stack.return_stack(filename)
  dataset = import_functions.sort_dataset(raw_dataset)
  raw_dataset_values = [row[-1] for row in raw_dataset]
  raw_dataset_features = [row[0:-1] for row in raw_dataset]
  dataset_values = [row[-1] for row in dataset]
  dataset_features = [row[0:-1] for row in dataset] 

  #print(len(raw_dataset))
  print(len(dataset))

  print(' *** Creating Regression Forest *** \n')
  forest = RandomForestRegressor(max_depth=4, n_estimators=2000, min_samples_leaf=9)
  
  #print("Fitting")
  forest.fit(dataset_features, dataset_values)
  
  #print("Scoring")
  #score = forest.score(dataset_features, dataset_values)
  
  #print('    Score:' + str(score) + '\n')
  #importance = forest.feature_importances_
  #print('    Feature Importance:' + str(importance) + '\n')
  
  print(' *** Making Predictions *** \n')
  predictions = forest.predict(raw_dataset_features).tolist()
 
  print(' *** Writing Predictions to file *** \n')
  output_filename = export_functions.generate_filenames(filename)
  export_functions.output_tif(predictions, shape, output_filename, geotrans, proj)

  print(' *** Finished *** ')
  return

#make_prediction('./train/1.shp')
