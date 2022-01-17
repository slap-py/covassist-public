import time
import json

data = open('data\Vaccines.gov__COVID-19_vaccinating_provider_locations.csv','r')
data = data.read()

data = data.split('\n')
datapoints = data[0]
data_out = []
#Category,Unnamed Column														
for line in data:
    comma = line.split(',')
    #print(comma)
    #time.sleep(1)
    print(len(data_out))
    try:
        data_out.append({
            'provider_location':comma[0],
            'guid_location':comma[1],
            'store_number':comma[2],
            'store_phone_number':comma[3],
            'store_name':comma[4],
            'street_names':[comma[5],comma[6]],
            'city':comma[7],
            'state':comma[8],
            'zip_code':comma[9],
            'hours':[comma[10],comma[11],comma[12],comma[13],comma[14],comma[15],comma[15]],
            'website':comma[16],
            'pre_screen':comma[17], # unknown datapoint
            'insurance':comma[18], # todo: convert to boolean
            'walkins':comma[19], # todo: convert to boolean
            'notes':comma[20],
            'ndc': comma[21], # unknown datapoint
            'vaccine_types':comma[22],
            'supply_level':comma[23], #conflicts with quantity
            'quantity':comma[24],
            'lat':comma[25],
            'lon':comma[26],
            'category':comma[27], #unknown datapoint
            'unnamed_column':comma[28], #unknown datapoint
            })
    except:
        file = open('data/vaccines.json','w')
        file.write(json.dumps(data_out))
        file.close()
        print('write complete')

file = open('data/vaccines.json','w')
file.write(json.dumps(data_out))
file.close()
print('write complete')
