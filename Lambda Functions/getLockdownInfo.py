import json
import sys
import pandas as pd
import requests
import boto3
from bs4 import BeautifulSoup
from datetime import datetime as dt, date, timedelta
from decimal import Decimal
import time


def test(x):
    today = date.today()
    start = today - timedelta(days=today.weekday())
    start = dt.combine(start, dt.min.time())
    test_date = dt.strptime(x.strip(), "%Y-%m-%d")
    return test_date >= start

def getCode(country, countries_codes):
    response = countries_codes.get_item(Key={
      'country': country,
    })
    return response['Item']['code']

def lambda_handler(event, context):
    # Getting correct table
    url = "https://en.wikipedia.org/wiki/COVID-19_lockdowns"
    df = pd.read_html(url, match='COVID-19 pandemic lockdowns')
    df = df[0]
    
    # Removing unneccesary table headers
    df.columns = df.columns.get_level_values(2)    
    
    # Including only national lockdowns in dataframe
    df = df.loc[df['Level'] == "National"]
    
    # Removing brackets with hyperlinks from dates
    df = df.replace(r"\[.*?\]","",regex=True)
    df = df.replace(r"\(.*?\)","",regex=True)
    
    # Replacing empty spaces or NaN with 0
    df = df.fillna(0)
    
    # Removing unneccesary columns
    df.drop('Place', inplace=True, axis=1)
    df.drop('Start date', inplace=True, axis=1)
    df.drop('Length (days)', inplace=True, axis=1)
    df.drop('Level', inplace=True, axis=1)
    df.drop('Total length (days)', inplace=True, axis=1)
    
    # Renaming columns
    df.columns = ['Country', 'L1', 'L2', 'L3']
    
    result = []
    for index, row in df.iterrows():
        if row['L2'] == 0:
            result.append(row['L1'])
        elif row['L3'] == 0:
            result.append(row['L2'])
        else:
            result.append(row['L3'])
            
    df['Lockdown End'] = result
    df.drop('L1', inplace=True, axis=1)
    df.drop('L2', inplace=True, axis=1)
    df.drop('L3', inplace=True, axis=1)
    df['Lockdown End'] = df['Lockdown End'].replace(['2020-04-21to 2020-05-04'], "2020-05-04")
    df['Lockdown End'] = df['Lockdown End'].replace(['2021-03-01 to 2021-04-19'], "2021-04-19")
    df['Lockdown End'] = df['Lockdown End'].replace(['not set'], 0)
    df.drop( df[ df['Lockdown End'] == 0 ].index , inplace=True)
    df['Current Lockdown?'] = df['Lockdown End'].apply(test)
    df = df.loc[df['Current Lockdown?'] == True]
    print(df)
    
    
    # Instanciating connection objects with DynamoDB using boto3 dependency
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')
    
    # Getting the table objects
    countries_lockdowns = dynamodb.Table('country_lockdowns')
    countries_codes = dynamodb.Table('country_codes')

    try:
        with countries_lockdowns.batch_writer() as batch:
            for index, row in df.iterrows():
                chunk = { 
                    'date': dt.now().strftime("%d/%m/%y"),
                    'code': getCode(row['Country'], countries_codes),
                    'country': row['Country'],
                    'lockdownEndDate': str(row['Lockdown End']),
                    'fact': "Yes",
                    'ttl': Decimal(str(time.time() + 604800))
                }
                batch.put_item(Item=chunk)
        return {
            'statusCode': 200,
            'body': json.dumps('Success saving the global COVID-19 cases')
        }
    except Exception as e:
        print('Closing lambda function')
        print(e)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno

        print("Exception type: ", exception_type)
        print("File name: ", filename)
        print("Line number: ", line_number)
        return {
            'statusCode': 400,
            'body': json.dumps('Error saving the global COVID-19 cases')
        }
        
