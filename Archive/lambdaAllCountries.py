import json
import pandas as pd
from datetime import datetime
import boto3
from decimal import Decimal

def lambda_handler(event, context):
    # TODO implement
    country = event['country']
    #country = event["queryStringParameters"]['country']
    
    url = 'https://covid19.who.int/WHO-COVID-19-global-table-data.csv'

    df = pd.read_csv(url)
    
    df = df.filter(['Name', 'Cases - newly reported in last 7 days per 100000 population', 'Cases - newly reported in last 24 hours'])
    df.dropna(axis = 0, how = 'any', thresh = None, subset = None, inplace = True)
    
    cases_100000 = df.loc[df['Name']==f'{country}', 'Cases - newly reported in last 7 days per 100000 population'].values[0]
    cases_24 = df.loc[df['Name']==f'{country}', 'Cases - newly reported in last 24 hours'].values[0]
    
    # Instanciating connection objects with DynamoDB using boto3 dependency
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')
    
    # Getting the table the table ukcases object
    countries = dynamodb.Table('Countries')
    
    
    # Putting a try/catch to log to user when some error occurs
    try:
        # countries.put_item(
        #   Item={ 
        #         'date': datetime.now().strftime('%Y-%m-%d'),
        #         'country': country,
        #         'dailyCases': int(cases_24),
        #         'percentage': Decimal(str(25)),
        #         'rate': Decimal(str(cases_100000))
        #     }
        # )
        with countries.batch_writer() as batch:
            for index, row in df.iterrows():
                chunk = { 
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'country': row['Name'],
                    'dailyCases': row['Cases - newly reported in last 24 hours'],
                    'percentage': str(25),
                    'rate': Decimal(str(row['Cases - newly reported in last 7 days per 100000 population']))
                }
                batch.put_item(Item=chunk)
        return {
            'statusCode': 200,
            'body': json.dumps('Succesfully inserted uk cases!')
        }
    except Exception as e:
        print('Closing lambda function')
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps('Error saving the uk cases')
        }
