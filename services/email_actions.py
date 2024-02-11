from lib.filters import Filters
from lib.email_string import EmailString
from dateutil import tz
from datetime import timedelta, datetime
from googleapiclient.discovery import build
from lib.google_api_batch_request import GmailBatchRequest

class EmailActions:
  def __init__(self, rule: dict, emails: any, creds: any) -> None:
    self.filtered_by_field = {}
    self.rule = rule
    self.creds = creds
    self.filtered_emails = []
    self.emails = emails

  def filters(self):
    for field in Filters().fields():
      if field['filter_key'] in self.rule:
        if field['type'] == 'date':
          self.filtered_by_field[field['key']] = self.filter_by_date(field)
        elif field['type'] == 'email':
          self.filtered_by_field[field['key']] = self.filter_by_email(field)
        else:
          self.filtered_by_field[field['key']] = self.filter_by_string(field)
      else:
        self.filtered_by_field[field['key']] = []
    if self.rule['any_or_all'] == 'any':
      # Get all union of all message_id of  filtered_by_field flatten values and unique values
      for field in Filters().fields():
        self.filtered_emails += self.filtered_by_field[field['key']]
      self.filtered_emails = list(set([email.id for email in self.filtered_emails]))
    else:
      # Get all intersection of all message_id of  filtered_by_field flatten values and unique values
      self.filtered_emails = set.intersection(*(set(item.id for item in sublist) for sublist in self.filtered_by_field.values() if sublist))
    return self.filtered_emails

  def filter_by_date(self, field: dict):
    field_rule = self.rule[field['filter_key']]
    time_diff = timedelta(days=int(field_rule['value'])) if field_rule['unit'] == 'days' else timedelta(
      weeks=field_rule['value']
    ) if field_rule['unit'] == 'weeks' else timedelta(
      months=field_rule['value']
    ) if field_rule['unit'] == 'months' else timedelta(
      years=field_rule['value']
    )
    field_date = datetime.now(tz=tz.tzlocal()) - time_diff
    if field_rule['operation'] == 'less_than':
      return list(filter(lambda x, field=field: getattr(x, field['key']) > field_date, self.emails))
    elif field_rule['operation'] == 'greater_than':
      return list(filter(lambda x, field=field: getattr(x, field['key']) < field_date, self.emails))

  def filter_by_email(self, field: dict):
    field_rule = self.rule[field['filter_key']]
    if field_rule['operation'] == 'equals' or field_rule['operation'] == 'not_equals':
      filtered_emails = []
      for email in self.emails:
        email_values = [
          EmailString(email).parse() for email in getattr(email, field['key']).split(',')
        ]
        for email_value in email_values:
          if field_rule['operation'] == 'equals':
            if email_value['email'] == field_rule['value'] or email_value['name'] == field_rule['value']:
              filtered_emails.append(email)
          else:
            if email_value['email'] != field_rule['value'] and email_value['name'] != field_rule['value']:
              filtered_emails.append(email)
      return filtered_emails
    elif field_rule['operation'] == 'contains':
      return list(
        filter(
          lambda x, field=field: field_rule['value'].lower() in getattr(x, field['key']).lower(), self.emails
        )
      )
    else:
      return list(
        filter(
          lambda x, field=field: field_rule['value'].lower() not in getattr(x, field['key']).lower(), self.emails
        )
      )

  def filter_by_string(self, field: dict):
    field_rule = self.rule[field['filter_key']]
    if field_rule['operation'] == 'equals':
      return list(filter(lambda x, field=field: getattr(x, field['key']) == field_rule['value'], self.emails))
    elif field_rule['operation'] == 'not_equals':
      return list(filter(lambda x, field=field: getattr(x, field['key']) != field_rule['value'], self.emails))
    elif field_rule['operation'] == 'contains':
      return list(
        filter(
          lambda x, field=field: field_rule['value'].lower() in getattr(x, field['key']).lower(), self.emails
        )
      )
    else:
      return list(
        filter(
          lambda x, field=field: field_rule['value'].lower() not in getattr(x, field['key']).lower(), self.emails
        )
      )

  def mark_as_read(self):
    service = build('gmail', 'v1', credentials=self.creds)
    requests = []
    for mail_id in self.filtered_emails:
      requests.append(
        service.users().messages().modify(userId='me', id=mail_id, body={'removeLabelIds': ['UNREAD']})
      )
    GmailBatchRequest(service, self.creds, self.callback).execute(requests)

  def mark_as_unread(self):
    service = build('gmail', 'v1', credentials=self.creds)
    requests = []
    for mail_id in self.filtered_emails:
      requests.append(
        service.users().messages().modify(userId='me', id=mail_id, body={'addLabelIds': ['UNREAD']})
      )
    GmailBatchRequest(service, self.creds, self.callback).execute(requests)

  def move(self, folder: dict):
    service = build('gmail', 'v1', credentials=self.creds)
    requests = []
    for mail_id in self.filtered_emails:
      mail = list(filter(lambda x: x.id == mail_id, self.emails))[0]
      add_labels = [folder['id']]
      remove_labels = mail.labels.split(',')
      if folder['id'] in remove_labels:
        remove_labels.remove(folder['id'])
      requests.append(
        service.users().messages().modify(
          userId='me',
          id=mail_id,
          body={
            'addLabelIds': add_labels,
            'removeLabelIds': remove_labels
          }
        )
      )
    GmailBatchRequest(service, self.creds, self.callback).execute(requests)

  def callback(self, _request_id, response, _exception):
    print(response)
