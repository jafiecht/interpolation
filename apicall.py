import geopandas
import json
import root

rawInput = open('data/apicall/input_object.json')
data = json.load(rawInput)

root.validate_predict(data)
