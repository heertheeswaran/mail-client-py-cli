import requests

class GmailApi:
  def __init__(self, creds):
    self.creds = creds
  
  def modify_message(self, msg_id, add_labels, remove_labels):
    url = f'https://www.googleapis.com/gmail/v1/users/me/messages/{msg_id}/modify'
    headers = {
      'Authorization': f'Bearer {self.creds.token}',
      'Content-Type': 'application/json'
    }
    data = {
      'addLabelIds': add_labels,
      'removeLabelIds': remove_labels
    }
    response = requests.post(url, headers=headers, json=data, timeout=10)
    return response.json()
