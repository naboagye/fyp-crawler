import json
import boto3
from datetime import datetime as dt
import datetime

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    countries = dynamodb.Table('country_covid_cases')
    
    response = countries.get_item(Key={
      'date': event['date'],
      'code': event['code']
    })
    
    response2 = countries.get_item(Key={
      'date': (dt.fromisoformat(event['date'])-datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
      'code': event['code']
    })
    
    # Use yesterday's data if no data is present yet for today
    if 'Item' not in response:
        print("oh no")
        response = countries.get_item(Key={
            'date': (dt.fromisoformat(event['date'])-datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            'code': event['code']
        })
        response2 = countries.get_item(Key={
          'date': (dt.fromisoformat(event['date'])-datetime.timedelta(days=2)).strftime("%Y-%m-%d"),
          'code': event['code']
        })
    
    # Calculate +/- difference for number of cases and rate    
    rateDiff = round(float(response["Item"]["rate"]) - float(response2["Item"]["rate"]), 2)
    casesDiff = int(response["Item"]["dailyCases"]) - int(response2["Item"]["dailyCases"])
    
    if rateDiff < 0:
        rateDiff = str(rateDiff)[1:]
        rateDiffInd = "down"
    else:
        rateDiffInd = "up"
    
    if casesDiff < 0:
        casesDiff = str(casesDiff)[1:]
        casesDiffInd = "down"
    else:
        casesDiffInd = "up"
        
    return {
        'statusCode': 200,
        "headers": {
            "Content-Type": "application/json"
        },
        'body':  {"Item":response, "rateDiff":rateDiff, "rateDiffInd":rateDiffInd, "casesDiff":casesDiff, "casesDiffInd": casesDiffInd}
    }
