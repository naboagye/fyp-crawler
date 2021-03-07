import json
import boto3


def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    travel_info = dynamodb.Table('travel_info')
    
    response = travel_info.get_item(Key={
      'date': event["queryStringParameters"]['date'],
      'country': event["queryStringParameters"]['country']
    })
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
