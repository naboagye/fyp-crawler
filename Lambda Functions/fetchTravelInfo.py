import json
import boto3
from datetime import datetime as dt
import datetime

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    travel_info = dynamodb.Table('country_travel_advice')
    
    # querying DB table using parameters of API call (date and country code)
    response = travel_info.get_item(Key={
      'date': event['date'],
      'code': event['code']
    })
    
    try:
        # check if DB table has been updated with information dated today otherwise use yesterdays data
        if 'Item' not in response:
            response = travel_info.get_item(Key={
                'date': (dt.fromisoformat(event['date'])-datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
                'code': event['code']
            })
        return {
            'statusCode': 200,
            "headers": {
                "Content-Type": "application/json"
            },
            'body':  response
        }
    except Exception as e:
        print('Closing lambda function')
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps('Error retrieving the travel info')
        }
    