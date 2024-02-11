import json

class Filters:
  def __init__(self) -> None:
    with open('config/filters.json', 'r', encoding='utf-8') as filters:
      self.filters = json.load(filters)

  def fields(self):
    return self.filters['fields']

  def get_field(self, field_name):
    return list(filter(lambda x: x['name'] == field_name, self.fields()))[0]

  def rules(self):
    with open('config/rules.json', 'r', encoding='utf-8') as rules:
      return json.load(rules)
