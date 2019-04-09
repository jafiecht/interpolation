import geopandas
import json
import root

rawInput = open('data/apicall/input_object.json')
data = json.load(rawInput)

response = root.validate_predict(data)

print('\n   Response: ', response)
