import json
import boto3
from botocore.exceptions import ClientError
import requests
from datetime import datetime
from string import Template

def sendEmail(email, destination, dailyCases, rate, date, travelInfo, link):
    SENDER = "alerts@strataflights.co.uk"

    RECIPIENT = email

    AWS_REGION = "eu-west-2"
    
    SUBJECT = f"Your Daily Update on the COVID-19 Situation in {destination}"
    
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = (f"Here is the latest on the COVID-19 Situation in {destination}!\r\n"
                 f"Information correct as of $date"
                f"Number of COVID-19 cases in the last 24 hours: {dailyCases}"
                f"Weekly Rate of COVID-19 cases per 100,000 people: {rate}"
                f"Latest Travel Advice:\r\n"
                f"{travelInfo}\r\n"
                f"{link}"
                )
    
    html_template = Template("""<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="x-apple-disable-message-reformatting">
  <title></title>
  <!--[if mso]>
  <style>
    table {border-collapse:collapse;border-spacing:0;border:none;margin:0;}
    div, td {padding:0;}
    div {margin:0 !important;}
  </style>
  <noscript>
    <xml>
      <o:OfficeDocumentSettings>
        <o:PixelsPerInch>96</o:PixelsPerInch>
      </o:OfficeDocumentSettings>
    </xml>
  </noscript>
  <![endif]-->
  <style>
    table, td, div, h1, p {
      font-family: Arial, sans-serif;
    }
    @media screen and (max-width: 530px) {
      .unsub {
        display: block;
        padding: 8px;
        margin-top: 14px;
        border-radius: 6px;
        background-color: #555555;
        text-decoration: none !important;
        font-weight: bold;
      }
      .col-lge {
        max-width: 100% !important;
      }
    }
    @media screen and (min-width: 531px) {
      .col-sml {
        max-width: 27% !important;
      }
      .col-lge {
        max-width: 73% !important;
      }
    }
  </style>
</head>
<body style="margin:0;padding:0;word-spacing:normal;background-color:#E6F1F5;">
  <div role="article" aria-roledescription="email" lang="en" style="text-size-adjust:100%;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;background-color:#E6F1F5;">
    <table role="presentation" style="width:100%;border:none;border-spacing:0;">
      <tr>
        <td align="center" style="padding:0;">
          <!--[if mso]>
          <table role="presentation" align="center" style="width:600px;">
          <tr>
          <td>
          <![endif]-->
          <table role="presentation" style="width:94%;max-width:600px;border:none;border-spacing:0;text-align:left;font-family:Arial,sans-serif;font-size:16px;line-height:22px;color:#363636;">
            <tr>
              <td style="padding:40px 30px 30px 30px;text-align:center;font-size:24px;font-weight:bold;">
                <a href="http://www.strataflights.co.uk" style="text-decoration:none;"><img src="https://strataflights.co.uk/logo500.png" width="165" alt="Logo" style="width:80%;max-width:165px;height:auto;border:none;text-decoration:none;color:#ffffff;"></a>
              </td>
            </tr>
            <tr>
              <td style="padding:30px;background-color:#ffffff;">
                <h1 style="margin-top:0;margin-bottom:16px;font-size:26px;line-height:32px;font-weight:bold;letter-spacing:-0.02em;">Here is the latest on the COVID-19 Situation in $destination!</h1>
                <p style="margin:0;">Information correct as of $date</p>
                <p style="margin:0;">Number of COVID-19 cases in the last 24 hours: $dailyCases</p>
                <p style="margin:0;">Weekly Rate of COVID-19 cases per 100,000 people: $rate</p>
                <p style="margin:0;">Latest Travel Advice:</p>
                <p style="margin:0;">$travelInfo</p>
                <p style="margin:0;">$link</p>
              </td>
            </tr>
            <tr>
              <td style="padding:0;font-size:24px;line-height:28px;font-weight:bold;">
                <a href="http://www.example.com/" style="text-decoration:none;"><img src="https://assets.codepen.io/210284/1200x800-2.png" width="600" alt="" style="width:100%;height:auto;display:block;border:none;text-decoration:none;color:#363636;"></a>
              </td>
            </tr>
            <tr>
              <td style="padding:35px 30px 11px 30px;font-size:0;background-color:#ffffff;border-bottom:1px solid #f0f0f5;border-color:rgba(201,201,207,.35);">
                <!--[if mso]>
                <table role="presentation" width="100%">
                <tr>
                <td style="width:145px;" align="left" valign="top">
                <![endif]-->
                <div class="col-sml" style="display:inline-block;width:100%;max-width:145px;vertical-align:top;text-align:left;font-family:Arial,sans-serif;font-size:14px;color:#363636;">
                  <img src="https://assets.codepen.io/210284/icon.png" width="115" alt="" style="width:80%;max-width:115px;margin-bottom:20px;">
                </div>
                <!--[if mso]>
                </td>
                <td style="width:395px;padding-bottom:20px;" valign="top">
                <![endif]-->
                <div class="col-lge" style="display:inline-block;width:100%;max-width:395px;vertical-align:top;padding-bottom:20px;font-family:Arial,sans-serif;font-size:16px;line-height:22px;color:#363636;">
                  <p style="margin-top:0;margin-bottom:12px;">Want more flight destinations inspo.</p>
                  <p style="margin-top:0;margin-bottom:18px;">CLick below to go to our Flight Ideas page!</p>
                  <p style="margin:0;"><a href="https://example.com/" style="background: #2daae2; text-decoration: none; padding: 10px 25px; color: #ffffff; border-radius: 4px; display:inline-block; mso-padding-alt:0;text-underline-color:#ff3884"><!--[if mso]><i style="letter-spacing: 25px;mso-font-width:-100%;mso-text-raise:20pt">&nbsp;</i><![endif]--><span style="mso-text-raise:10pt;font-weight:bold;">Claim yours now</span><!--[if mso]><i style="letter-spacing: 25px;mso-font-width:-100%">&nbsp;</i><![endif]--></a></p>
                </div>
                <!--[if mso]>
                </td>
                </tr>
                </table>
                <![endif]-->
              </td>
            </tr>
            <tr>
              <td style="padding:30px;text-align:center;font-size:12px;background-color:#404040;color:#cccccc;">
                <p style="margin:0 0 8px 0;"><a href="http://www.facebook.com/" style="text-decoration:none;"><img src="https://assets.codepen.io/210284/facebook_1.png" width="40" height="40" alt="f" style="display:inline-block;color:#cccccc;"></a> <a href="http://www.twitter.com/" style="text-decoration:none;"><img src="https://assets.codepen.io/210284/twitter_1.png" width="40" height="40" alt="t" style="display:inline-block;color:#cccccc;"></a></p>
                <p style="margin:0;font-size:14px;line-height:20px;">&reg; Strata Flights 2021<br><a class="unsub" href="http://www.example.com/" style="color:#cccccc;text-decoration:underline;">Unsubscribe instantly</a></p>
              </td>
            </tr>
          </table>
          <!--[if mso]>
          </td>
          </tr>
          </table>
          <![endif]-->
        </td>
      </tr>
    </table>
  </div>
</body>
</html>
                """)
                
    # The HTML body of the email.
    html = html_template.substitute(date=date, dailyCases=dailyCases, rate=rate, destination=destination, travelInfo=travelInfo, link=link)
    BODY_HTML = html        
    
    # The character encoding for the email.
    CHARSET = "UTF-8"
    
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
        
    
def scan_table(dynamo_client, *, TableName, **kwargs):
    #Generates all the items in a DynamoDB table.
    paginator = dynamo_client.get_paginator("scan")

    for page in paginator.paginate(TableName=TableName, **kwargs):
        yield from page["Items"]

def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb')
    today = datetime.now().strftime('%Y-%m-%d')
    AWS_REGION = "eu-west-2"
    ses_client = boto3.client('ses',region_name=AWS_REGION)
    
    for item in scan_table(dynamodb, TableName="Subscriptions"):
        email = item['email']['S']
        destination = item['destination']['S']
        code = item['code']['S']
        url = f'https://hmbrr2y0jg.execute-api.eu-west-2.amazonaws.com/dev?code={code}&date={today}'
        response = requests.get(url)
        rate = response.json()['body']['Item']['Item']['rate']
        cases = response.json()['body']['Item']['Item']['dailyCases']
        
        url2 = f'https://3tmuo3iuhk.execute-api.eu-west-2.amazonaws.com/dev?code={code}&date={today}'
        response2 = requests.get(url2)
        travelInfo = response2.json()['body']['Item']["info"]
        link = response2.json()['body']['Item']["links"]
        
        res = ses_client.get_identity_verification_attributes(
          Identities=[
              email,
          ]
        )
    
        if res['VerificationAttributes'][email]['VerificationStatus'] == "Success":
          sendEmail(email, destination, cases, rate, today, travelInfo, link)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
