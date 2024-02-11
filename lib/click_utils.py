import click

def list_options(options, prompt_message, input_message):
  click.secho(prompt_message, fg='green')
  i = 0
  for option in options:
    if isinstance(option, dict):
      if 'option' in option:
        click.secho(f'{i + 1}. {option["option"].capitalize()}', fg='blue')
      else:
        click.secho(f'{i + 1}. {option}', fg='blue')
    else:
      click.secho(f'{i + 1}. {option.capitalize()}', fg='blue')
    i += 1
  index = int(click.prompt(input_message, type=int))
  if index > len(options):
    raise ValueError('Invalid option')
  option = options[index - 1]
  return option
