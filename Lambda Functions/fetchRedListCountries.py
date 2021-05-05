import json
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime as dt
import datetime

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    red_list_countries = dynamodb.Table('red_list_countries')
    
    # querying DB table using parameters of API call (date)
    dateInput = event['date']
    
    response = red_list_countries.query(KeyConditionExpression=Key('date').eq(str(dateInput)))

    if not response['Items']:
        print("No data yet for today")
        dateInput = (dt.fromisoformat(dateInput)-datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        response = red_list_countries.query(KeyConditionExpression=Key('date').eq(str(dateInput)))

    codes = []
    countries = []
    for res in response['Items']:
        codes.append(res["code"])
        countries.append(res["country"])
        
    return {
        'statusCode': 200,
        "headers": {
            "Content-Type": "application/json"
        },
        'body': {"codes": codes, "countries": countries}
    }
