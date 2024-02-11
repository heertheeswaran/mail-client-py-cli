from googleapiclient.discovery import build

class EmailFolder:
  def __init__(self, creds) -> None:
    self.creds = creds

  def list(self):
    service = build('gmail', 'v1', credentials=self.creds)
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    return [{'id': label['id'], 'option': label['name']} for label in labels if self.show_label(label)]
  
  def show_label(self, label):
    if label['type'] != 'user':
      if 'messageListVisibility' in label and label['messageListVisibility'] == 'hide':
        return False
      if 'labelListVisibility' in label and label['labelListVisibility'] == 'labelHide':
        return False
    return True
