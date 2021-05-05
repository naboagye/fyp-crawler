import json
import boto3

def lambda_handler(event, context):
    # Create a new SES resource and specify a region.
    AWS_REGION = "eu-west-2"
    client = boto3.client('ses',region_name=AWS_REGION)

    ### Unhighlight to update template
    # response = client.update_custom_verification_email_template(
    #   TemplateName="verifyNewUser",
    #   FromEmailAddress="alerts@strataflights.co.uk",
    #   TemplateSubject="Please confirm your email address",
    #   TemplateContent="""<html><head></head><body style='font-family:sans-serif;'><h1 style='text-align:center'>Please confirm your email address</h1><p>We here at Strata Flights are happy to have you on board! There's just one last step to complete before we can start sending you weekly updates. Just click the following link to verify your email address. Once we confirm that you're really you, we can go ahead and keep you updated on the COVID-19 situation for your destination.</p></body></html>""",
    #   SuccessRedirectionURL="https://www.strataflights.co.uk/success",
    #   FailureRedirectionURL="https://www.strataflights.co.uk/failure"
    # )
    
    response = client.send_custom_verification_email(
        EmailAddress=event['to'],
        TemplateName='verifyNewUser'
    )
    
    
    dynamodb = boto3.resource('dynamodb')
    db_client = boto3.client('dynamodb')
    
    subs = dynamodb.Table('Subscriptions')
    
    chunk = { 
        "email": event['to'],
        "destination": event['destination'],
        "code": event['code']
    }
    subs.put_item(Item=chunk)

    return {
        'statusCode': 200,
        'body': response
    }
