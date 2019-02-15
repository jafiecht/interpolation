import geopandas as gpd
from sklearn.model_selection import KFold

soilfp = './combined_soil.shp'
traindir = './train/'
testdir = './test/'

data = gpd.read_file(soilfp)
index = list(range(data.shape[0]))

i = 1
kfold = KFold(10, True, 1)
for train, test in kfold.split(index):
  test_indices = test.tolist()
  train_indices = train.tolist()
  test_df = data.iloc[test_indices]
  train_df = data.iloc[train_indices]
  test_df.to_file(testdir + str(i) + '.shp')
  train_df.to_file(traindir + str(i) + '.shp')
  i += 1
  

