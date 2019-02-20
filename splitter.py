#This file splits the main file into k
#train/test folds, then writes them to file

#Imports
import geopandas as gpd
from sklearn.model_selection import KFold

#Filepaths
soilfp = './combined_soil.shp'
traindir = './train/'
testdir = './test/'

#Read in the original data
data = gpd.read_file(soilfp)

#Create an index list for the data library to split on
index = list(range(data.shape[0]))

#kfold parameters
kfold = KFold(10, True, 1)

#Write the train and test indices to file
i = 1
for train, test in kfold.split(index):
  test_indices = test.tolist()
  train_indices = train.tolist()
  test_df = data.iloc[test_indices]
  train_df = data.iloc[train_indices]
  test_df.to_file(testdir + str(i) + '.shp')
  train_df.to_file(traindir + str(i) + '.shp')
  i += 1
  
