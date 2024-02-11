from .filters import Filters
from dateutil import parser, tz

class EmailResponseParser:
  def __init__(self, email_data):
    self.email_data = email_data
    self.data = {}
  
  def parse(self):
    fields = Filters().fields()
    self.data['message_id'] = self.email_data['id']
    self.data['id'] = self.email_data['id']
    self.data['thread_id'] = self.email_data['threadId']
    self.data['labels'] = ','.join([label for label in self.email_data['labelIds'] if label != 'UNREAD'])
    for field in fields:
      header_field = list(
        filter(lambda x, field=field: x['name'] == field['name'], self.email_data['payload']['headers'])
      )
      if len(header_field) > 0:
        if field['name'] == 'Received':
          value = header_field[0]['value'].split(';')[1].strip()
        else:
          value = header_field[0]['value'].strip().replace('"', '')

        if field['type'] == 'date':
          value = parser.parse(value).astimezone(tz.tzutc())
        self.data[field['key']] = value
      else:
        self.data[field['key']] = ''
    return self.data
