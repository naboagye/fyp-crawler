import json
import boto3
import requests
from decimal import Decimal

def lambda_handler(event, context):
    # TODO implement
    # Instanciating connection objects with DynamoDB using boto3 dependency
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')
    
    # Getting the table the table ukcases object
    tableUKCases = dynamodb.Table('ukCases')
    
    ENDPOINT = event['url']
    AREA_TYPE = "overview"
    AREA_NAME = "england"
    
    filters = [
        f"areaType={ AREA_TYPE }"
    ]
    
    structure = {
        "date": "date",
        "dailyCases": "newCasesByPublishDate",
        "percentage": "newCasesByPublishDateChangePercentage",
    }
    
    rate = {
        "rate": "newCasesBySpecimenDateRollingRate"
    }
    
    api_params = {
        "filters": str.join(";", filters),
        "structure": json.dumps(structure, separators=(",", ":")),
        "latestBy": "newCasesByPublishDate"
    }
    
    api_params2 = {
        "filters": str.join(";", filters),
        "structure": json.dumps(rate, separators=(",", ":")),
        "latestBy": "newCasesBySpecimenDateRollingRate"
    }
    
    formats = [
        "json"
    ]


    for fmt in formats:
        api_params["format"] = fmt
        response = requests.get(ENDPOINT, params=api_params, timeout=10)
        assert response.status_code == 200, f"Failed request for {fmt}: {response.text}"
        res = response.json()
        
        response2 = requests.get(ENDPOINT, params=api_params2, timeout=10)
        assert response2.status_code == 200, f"Failed request for {fmt}: {response.text}"
        res2 = response2.json()
        
        date = res["data"][0]["date"]
        dailyCases = res["data"][0]["dailyCases"]
        percentage = res["data"][0]["percentage"]
        rate = res2["data"][0]["rate"]
    
    
    # Putting a try/catch to log to user when some error occurs
    try:
        tableUKCases.put_item(
           Item={
                'date': date,
                'dailyCases': int(dailyCases),
                'percentage': Decimal(str(percentage)),
                'rate': Decimal(str(rate))
            }
        )
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
