import boto3
import json
import requests
from datetime import datetime
import json
import time 

# connect to AWS Kinesis
my_stream_name = 'maryland_weather_record'
kinesis_client = boto3.client('kinesis',
                              region_name='',
                              aws_access_key_id='',
                              aws_secret_access_key=''
                             )

#request data from weather rest API
token = 'vhYZMeOovHYCWBghoHYNLUFwwBjmYzxP'
header = dict(token=token)
location_id = 24 # Maryland id
url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/stations?locationid=FIPS:'+str(location_id)+'&limit=1000'
r = requests.get(url, headers=header)
d = json.loads(r.text)

#filter the stations that has data in our desire date range
station_id = []
station_name = []
for item in d['results']:
    min_date = datetime.strptime(item['mindate'], "%Y-%m-%d")
    max_date = datetime.strptime(item['maxdate'], "%Y-%m-%d")
    
    start_date = datetime.strptime('2020-10-01', "%Y-%m-%d")
    end_date = datetime.strptime('2020-10-31', "%Y-%m-%d")

    if (max_date >= end_date) and (min_date <= start_date):
        station_id.append(item['id'])
        station_name.append(item['name'])


#retrieve data from the filtered stations list
count = 0
for i in range(len(station_id)):
    sid = station_id[i]
    sname = station_name[i]
    url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&limit=1000&stationid='+sid+'&startdate=2021-10-01&enddate=2021-10-31'
    r = requests.get(url, headers={'token':token})
    d = json.loads(r.text)
    # the token only accept 5 requests per second
    time.sleep(0.3)
    try:
        for item in d['results']:
            if item['datatype']=='PRCP' or item['datatype']=='SNOW' or item['datatype']=='TMAX' or item['datatype']=='TMIN':
                json_data = {
                                'date': item['date'],
                                'stationid': sid,
                                'location': sname, 
                                'datatype': item['datatype'],
                                'value': item['value']
                            }
                time.sleep(0.01)
                put_response = kinesis_client.put_record(
                    StreamName=my_stream_name,
                    Data=json.dumps(json_data),
                    PartitionKey='stationid')
                
                count += 1
                print(count)            
    except:
        # station id is empty
        continue