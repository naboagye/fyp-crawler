import json
import boto3
import requests
from datetime import datetime

def lambda_handler(event, context):
    # TODO implement
    # Instanciating connection objects with DynamoDB using boto3 dependency
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')
    
    # Getting the table the table ukcases object
    tableUKCases = dynamodb.Table('ukCases')
    
    #country = event['country']
    country = event["queryStringParameters"]['country']
    
    url = f"https://api.covid19api.com/premium/travel/country/{country}"
    print(url)

    payload = {}
    headers = {
      'X-Access-Token': '5cf9dfd5-3449-485e-b5ae-70a60e997864'
    }
    
    response = requests.get(url, headers=headers, data = payload)
    output = response.json()['Notes'][0]['Note']
    #out = output1['Notes'][0]['Note']
    #print(output)
    
    # Putting a try/catch to log to user when some error occurs
    try:
        tableUKCases.update_item(
            Key={
                'date': datetime.now().strftime('%Y-%m-%d')
            },
            UpdateExpression="set policy=:p",
            ExpressionAttributeValues={
                ':p': output
            },
            ReturnValues="UPDATED_NEW"
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Succesfully inserted travel info!')
        }
    except Exception as e:
        print('Closing lambda function')
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps('Error saving the travel info')
        }
