import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import functools
import time


class emailFactory:
    def create_message(self, sender, to, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        return {'raw': raw_message}

    def send_message(self, service, user_id, message):
        try:
            message = (service.users().messages().send(userId=user_id, body=message).execute())
            print("Message Id: %s" % message['id'])
            return message
        except Exception as e:
            print("An error occurred: %s" % e)
            return None
    def __init__(self):
        # Set up the Gmail API credentials
        self.last_sent_email = None
        SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        # Create a Gmail service
        self.service = build('gmail', 'v1', credentials=creds)

    def compose_email(self, sender_email, receiver_email, subject, body):
        message = self.create_message(sender_email, receiver_email, subject, body)
        self.send_message(self.service, 'me', message)

