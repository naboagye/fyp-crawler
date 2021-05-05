import json
from datetime import datetime
import time
import boto3
from decimal import Decimal
import requests
from bs4 import BeautifulSoup
import sys
import re

def getCode(country, countries_codes):
    response = countries_codes.get_item(Key={
      'country': re.sub(r" ?\([^)]+\)", "", country),
    })
    print(response)
    if 'Item' in response:
        return response['Item']['code']
    else:
        return "n/a"
    
def lambda_handler(event, context):
    # Instanciating connection objects with DynamoDB using boto3 dependency
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')
    
    # Getting the table object
    red_list_countries = dynamodb.Table('red_list_countries')
    countries_codes = dynamodb.Table('country_codes')
    
    URL = 'https://www.gov.uk/guidance/transport-measures-to-protect-the-uk-from-variant-strains-of-covid-19#red-list-travel-ban-countries'
    page = requests.get(URL)
    # find div elements with the 'govspeak' class
    soup = BeautifulSoup(page.content, 'html.parser').find('div', class_='govspeak')
    # find all list elements within the unordered list contained in the govspeak class div
    countries = soup.find_next('ul').find_all('li')

    try:
        with red_list_countries.batch_writer() as batch:
            for country in countries:
                chunk = { 
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'code': getCode(country.text, countries_codes),
                    'country': country.text,
                    'ttl': Decimal(str(time.time() + 604800))
                }
                batch.put_item(Item=chunk)
        return {
            'statusCode': 200,
            'body': json.dumps('Succesfully inserted uk cases!')
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
            'body': json.dumps('Error saving the uk cases')
        }
