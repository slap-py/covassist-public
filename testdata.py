import json


data = open(r'data\vaccines.json','r').read()

data = json.loads(data)

print(data[1])