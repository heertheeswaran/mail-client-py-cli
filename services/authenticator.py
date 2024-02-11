import os
import click
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Authenticator:
  def __init__(self) -> None:
    pass

  def is_authenticated(self) -> bool:
    return os.path.exists('secrets/token.json')
  
  def initiate(self):
    if self.is_authenticated():
      return self.get_credentials()
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
        'secrets/credentials.json',
        ['https://www.googleapis.com/auth/gmail.modify']
      )
      creds = flow.run_local_server(port=0)
      with open('secrets/token.json', 'w', encoding='utf-8') as token:
        token.write(creds.to_json())
      return creds

  def get_credentials(self):
    if self.is_authenticated():
      creds = Credentials.from_authorized_user_file('secrets/token.json')
      if not creds.valid:
        if creds.expired and creds.refresh_token:
          creds.refresh(Request())
      return creds
    else:
      return None
