
from __future__ import print_function
import pickle
import os.path
import pandas as pd
import base64

from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.multipart import MIMEMultipart


def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEMultipart('alternative')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    # Converting output to html format

    data_file1 = pd.read_csv(
        r'D:\\Problem\\Automation Effort\\ConfirmEmail\\Output Files\\output.csv')
    temp = ''
    for index, row in data_file1.iterrows():
        temp = temp+"<tr><td>"+row[1]+"</td><td>"+row[2] + \
            "</td><td>"+row[3]+"</td><td>"+str(row[4])+"</td></tr>"
    html = """\
    <html>
    <head></head>
        <body>
            <h2>AcknowledgeMent Form</h2>
            <p>Please find the below details</p>
            <table style="width:100%" border="1px solid black">
            <tr>
                <th>Participant ID</th>
                <th>Participant Name</th> 
                <th>File Type</th>
                <th>Status</th>
            </tr>
"""
    html = html+temp
    html = html+"</table></body></html>"
    # print(html)

# Record the MIME types of both parts - text/plain and text/html.
    part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
    message.attach(part2)
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    return {'raw': raw}


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']


def send_message(service, user_id, message):
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message


def send_status():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    sender_mail = "Provide the sender mail id"
    message = create_message('dummyemail1307@gmail.com',
                             sender_mail, 'Test Mail', 'Hi Pavan')
    send_message(service, 'dummyemail1307@gmail.com', message)
