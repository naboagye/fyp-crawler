import json
import boto3
from datetime import datetime as dt
import datetime

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    country_lockdowns = dynamodb.Table('country_lockdowns')
    
    # querying DB table using parameters of API call (date and country code)
    response = country_lockdowns.get_item(Key={
      'date': dt.strptime(event['date'],"%Y-%m-%d").strftime("%d/%m/%y"),
      'code': event['code']
    })
    
    try:
        # check if DB table has been updated with information dated today otherwise use yesterdays data
        if 'Item' not in response:
            response = country_lockdowns.get_item(Key={
                'date': (dt.fromisoformat(event['date'])-datetime.timedelta(days=1)).strftime("%d/%m/%y"),
                'code': event['code']
             })
            if 'Item' not in response:
                response = {"Item":{"fact":"No", "date": "N/A"},}
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