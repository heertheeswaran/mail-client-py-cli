import re

class EmailString:
  def __init__(self, email_string: str) -> None:
    self.email_string = email_string.strip()
    self.data = {}

  def parse(self):
    match = re.match(r'^(?P<name>.+?)\s*<\s*(?P<email>.+?)\s*>$', self.email_string)
    if match:
      self.data['name'] = match.group('name')
      self.data['email'] = match.group('email')
    else:
      self.data['name'] = self.email_string
      self.data['email'] = self.email_string
    return self.data
