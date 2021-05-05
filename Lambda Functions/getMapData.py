import json
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime as dt
import datetime

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    countries = dynamodb.Table('country_covid_cases')
    country_lockdowns = dynamodb.Table('country_lockdowns')
    
    # querying DB table using parameters of API call (date)
    dateInput = (event['date'])
    
    response = countries.query(KeyConditionExpression=Key('date').eq(str(dateInput)))
    
    if not response['Items']:
        print("No data yet for today")
        dateInput = (dt.fromisoformat(dateInput)-datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        response = countries.query(KeyConditionExpression=Key('date').eq(str(dateInput)))

    arr = []
    for res in response['Items']:
        ld_response = country_lockdowns.get_item(Key={
            'date': dt.strptime(dateInput,"%Y-%m-%d").strftime("%d/%m/%y"),
            'code': res["code"]
        })
        if 'Item' not in ld_response:
            ld_response = {"Item":{"fact":"No", "date": "N/A"},}
        arr.append({"code":res["code"], "dailyCases":res["dailyCases"], "rate":res["rate"] ,"lockdown": ld_response["Item"]["fact"]})
        
    return {
        'statusCode': 200,
        "headers": {
            "Content-Type": "application/json"
        },
        'body': arr
    }
