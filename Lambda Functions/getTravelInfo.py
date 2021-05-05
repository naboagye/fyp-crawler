import json
import boto3
import pandas as pd
import requests
from datetime import datetime
import time
from decimal import Decimal
import re
import os


def lambda_handler(event, context):
    API_KEY = os.environ['API_KEY']
    # Instanciating connection objects with DynamoDB using boto3 dependency
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')
    
    # Getting the table object
    travel_info = dynamodb.Table('country_travel_advice')
    
    payload = {}
    headers = {
      'X-Access-Token': API_KEY
    }
    
    url = 'https://api.covid19api.com/countries'
    response = requests.get(url, headers=headers, data = payload)
    df = pd.DataFrame.from_dict(json.loads(response.text))
    
    try:
        with travel_info.batch_writer() as batch:
            for index, row in df.iterrows():
                country = row['Slug']
                url = f"https://api.covid19api.com/premium/travel/country/{country}"
                response = requests.get(url, headers=headers, data = payload)
                if 'Notes' not in response.json():
                    output = "No data currently available"
                elif not response.json()['Notes']:
                    output = "No data currently available"
                else:
                    output = response.json()['Notes'][0]['Note']
                
                urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', output)
                notes = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', output)
                
                chunk = { 
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'code': row['ISO2'],
                    'country': row['Country'],
                    'info': notes,
                    "links": urls,
                    'ttl': Decimal(str(time.time() + 604800))
                }
                batch.put_item(Item=chunk)
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
