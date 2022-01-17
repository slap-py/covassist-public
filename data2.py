import csv
import json
output = []
with open('data\Vaccines.gov__COVID-19_vaccinating_provider_locations.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        output.append(row)

file = open('data/vaccines.json','w')
file.write(json.dumps(output))
file.close()



idxs = []
locs = []
currentIdx = 1000
for location in output:
    if location in locs:
        idx = idxs.index(location['loc_name'])
        locs[idx]['med_name']+= ', '+location['med_name']
    else:
        location['index'] = currentIdx
        print(currentIdx)
        currentIdx+=1
        locs.append(location)

file = open('data/vaccines.json','w')
file.write(json.dumps(locs))
file.close()