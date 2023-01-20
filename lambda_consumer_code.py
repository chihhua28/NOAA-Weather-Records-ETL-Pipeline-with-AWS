import json
import boto3
import base64

def lambda_handler(event, context):

    try: 
        dynamo_db = boto3.resource('dynamodb', region_name = '')
        precipitaiton_table = dynamo_db.Table('Precipitation')
        temperature_table = dynamo_db.Table('Temperature')

        for record in event['Records']:
            data = base64.b64decode(record['kinesis']['data']).decode('utf-8')
            data_json = json.loads(data)
            print(data_json)
            if data_json['datatype']=='PRCP':
                precipitaiton_table.update_item(
                    Key={'stationid': data_json['stationid'], 'date': data_json['date']},
                    UpdateExpression="set StationName=:l, PRCP=:p",
                    ExpressionAttributeValues={
                    ':l': data_json['location'],
                    ':p': data_json['value']}
                    )
                    
            elif data_json['datatype']=='SNOW':
                precipitaiton_table.update_item(
                    Key={'stationid': data_json['stationid'], 'date': data_json['date']},
                    UpdateExpression="set StationName=:l, SNOW=:s",
                    ExpressionAttributeValues={
                    ':l': data_json['location'],
                    ':s': data_json['value'] }
                    )
            elif data_json['datatype']=='TMIN':
                temperature_table.update_item(
                    Key={'stationid': data_json['stationid'], 'date': data_json['date']},
                    UpdateExpression="set StationName=:l, TMIN=:n",
                    ExpressionAttributeValues={
                    ':l': data_json['location'],
                    ':n': data_json['value'] }
                    )
            
            elif data_json['datatype']=='TMAX':
                temperature_table.update_item(
                    Key={'stationid': data_json['stationid'], 'date': data_json['date']},
                    UpdateExpression="set StationName=:l, TMAX=:x",
                    ExpressionAttributeValues={
                    ':l': data_json['location'],
                    ':x': data_json['value'] }
                    )
            
                

    except Exception as e:
            print(str(e))