from googleapiclient.discovery import build
from lib.google_api_batch_request import GmailBatchRequest
from lib.email_response_parser import EmailResponseParser
from .authenticator import Authenticator

class EmailCollector:
  def __init__(self, config: dict) -> None:
    self.config = config
    self.emails = []

  def collect(self):
    creds = Authenticator().get_credentials()
    if creds:
      service = build('gmail', 'v1', credentials=creds)
      count = self.config['count']
      limit = count if count < 100 else 100
      next_page_token = None
      while count > 0:
        results = service.users().messages().list(
          userId='me',
          maxResults=limit,
          labelIds=['INBOX'],
          pageToken= next_page_token
        ).execute()
        messages = results.get('messages', [])
        next_page_token = results.get('nextPageToken')
        requests = [service.users().messages().get(userId='me', id=message['id']) for message in messages]
        GmailBatchRequest(service, creds, self.callback).execute(requests)
        count -= 100

      return self.emails
    else:
      raise Exception('Not authenticated')
  
  def callback(self, _request_id, response, _exception):
    self.emails.append(EmailResponseParser(response).parse())
