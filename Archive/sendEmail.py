import json
import smtplib

# =============================================================================
# SEND EMAIL FUNCTION
# =============================================================================
def send_email():
    # Change the items with: ######Change Me#######
    gmail_user = 'naboagye13'
    gmail_app_password = "fgcoezxukmatdpnw"
    sent_from = gmail_user
    sent_to = ['alerts@strataflights.co.uk']
    sent_subject = "Hello World"
    sent_body = "Its me World"

    email_text = """\
From: %s
To: %s
Subject: %s
%s
""" % (sent_from, ", ".join(sent_to), sent_subject, sent_body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_app_password)
        server.sendmail(sent_from, sent_to, email_text.encode("utf-8"))
        server.close()
        print(email_text)
        print('Email sent!')
    except Exception as exception:
        print("Error: %s!\n\n" % exception)
# =============================================================================
# END OF SEND EMAIL FUNCTION
# =============================================================================
send_email()