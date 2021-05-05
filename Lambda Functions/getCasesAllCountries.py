import json
import pandas as pd
from datetime import datetime
import time
import boto3
from decimal import Decimal
import requests
import sys

def getCode(country, countries_codes):
    response = countries_codes.get_item(Key={
      'country': country,
    })
    return response['Item']['code']

def lambda_handler(event, context):
    url = 'https://covid19.who.int/WHO-COVID-19-global-table-data.csv'

    df = pd.read_csv(url)
    
    df = df.filter(['Name', 'Cases - newly reported in last 7 days per 100000 population', 'Cases - newly reported in last 24 hours'])
    df.dropna(axis = 0, how = 'any', thresh = None, subset = None, inplace = True)
    
    # Instanciating connection objects with DynamoDB using boto3 dependency
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')
    
    # Getting the table object
    countries = dynamodb.Table('country_covid_cases')
    countries_codes = dynamodb.Table('country_codes')
    
    # Putting a try/catch to log to user when some error occurs
    try:
        with countries.batch_writer() as batch:
            for index, row in df.iterrows():
                chunk = { 
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'code': getCode(row['Name'], countries_codes),
                    'country': row['Name'],
                    'dailyCases': str(row['Cases - newly reported in last 24 hours']),
                    'rate': str(row['Cases - newly reported in last 7 days per 100000 population']),
                    'ttl': Decimal(str(time.time() + 604800))
                }
                batch.put_item(Item=chunk)
        return {
            'statusCode': 200,
            'body': json.dumps('Succesfully inserted all cases!')
        }
    except Exception as e:
        print('Closing lambda function')
        print(e)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        line_number = exception_traceback.tb_lineno
        print("Exception type: ", exception_type)
        print("Line number: ", line_number)
        return {
            'statusCode': 400,
            'body': json.dumps('Error saving the all cases')
        }
        