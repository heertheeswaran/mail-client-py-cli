import click
import asyncio
from functools import update_wrapper
from prisma import Prisma
from services.authenticator import Authenticator
from services.email_collector import EmailCollector
from lib.filters import Filters
from lib.click_utils import list_options
from services.email_folder import EmailFolder
from services.email_actions import EmailActions

def coro(f):
  f = asyncio.coroutine(f)
  def wrapper(*args, **kwargs):
      loop = asyncio.get_event_loop()
      return loop.run_until_complete(f(*args, **kwargs))
  return update_wrapper(wrapper, f)

actions = ['read', 'unread', 'move']
@click.group()
def cli():
  pass

@click.command()
@click.option('--count', default=100, help='Number of emails to fetch')
@coro
async def collect(count):
  db = Prisma()
  await db.connect()
  if not Authenticator().is_authenticated():
    Authenticator().initiate()
  
  emails = EmailCollector({
    'count': count,
  }).collect()
  for mail in emails:
    await db.mailitem.upsert(where={
      'id': mail['id']
    }, data={
      'create': mail,
      'update': mail
    })
  click.secho(
    f'Collected {len(emails)} emails. To perform operations on the collected emails, use the `action` command',
    fg='green'
  )

@click.command()
@coro
async def action():
  try:
    creds = Authenticator().get_credentials()
    db = Prisma()
    await db.connect()
    rules = Filters().rules()
    rule = list_options(rules, f'There are {len(rules)} rules available. Choose one to perform an action', "Enter the number of the rule you want to perform an action on")
    mailitems = await db.mailitem.find_many()
    processor = EmailActions(rule, mailitems, creds)
    filtered_emails = processor.filters()
    click.secho(f'Found {len(filtered_emails)} emails matching the rule', fg='green')
    action_input = list_options(actions, 'Choose an action to perform', 'Enter the number of the action you want to perform')
    if action_input == 'read':
      processor.mark_as_read()
    elif action_input == 'unread':
      processor.mark_as_unread()
    elif action_input == 'move':
      folders = EmailFolder(creds).list()
      folder = list_options(folders, 'Choose a folder to move the emails to', 'Enter the number of the folder you want to move the emails to')
      name = folder['option']
      click.confirm(f'Are you sure you want to move the emails to {name}', abort=True)
      processor.move(folder)
      for mail_id in filtered_emails:
        await db.mailitem.update(where={
          'id': mail_id
        }, data={
          'labels': ','.join([folder['id']])
        })
      # processor.move()
  except ValueError as e:
    click.secho(str(e), fg='red')
    return

cli.add_command(collect)
cli.add_command(action)
if __name__ == '__main__':
  cli()
