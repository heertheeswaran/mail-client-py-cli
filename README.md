# Email Management CLI

This is a command-line interface (CLI) tool for managing and performing actions on emails. The tool is built using Python, leveraging the Prisma library for database interactions and click for the command line integration.

## Installation

To install the dependencies, clone the repository and navigate to the project directory:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Database Setup

The tool uses a SQLite database to store emails. To set up the database, run the following command:

```bash
mkdir tmp
./venv/bin/prisma db push
```

This command creates a SQLite database in the `tmp` directory and sets up the schema for the database.

### Setup Email Credentials

Create a new google app and create a new oauth desktop client. Then, download the credentials file and save it as `secrets/credentials.json` in the root directory of the project.

### Authentication

Once you run the `collect` command, the tool will prompt you to authenticate your email account. This will open a browser window to authenticate your email account and grant access to the tool.

This will create a `secrets/token.json` file in the root directory of the project, which will be used to authenticate your email account for future requests.

## Features

### Email Collection

To collect emails, use the following command:

```bash
python cli.py collect --count <number_of_emails_to_fetch>
```

This command fetches a specified number of emails and stores them in the database.

### Email Actions

Perform various actions on the collected emails using the `action` command:

```bash
python cli.py action
```

The tool prompts you to choose a rule to filter emails. After selecting a rule, you can choose from the following actions:

1. **Read**: Mark selected emails as read.
2. **Unread**: Mark selected emails as unread.
3. **Move**: Move selected emails to a specific folder.

### Rules

You can customize rules for email actions. Modify the `config/rules.json` file to define rules based on your criteria.

### Running the CLI

To run the CLI, execute the script. This will list all the commands and options available for the tool:

```bash
python cli.py
```

## Disclaimer

This tool is designed for managing emails programmatically. Ensure that you understand the actions being performed, especially when moving emails or marking them as read/unread, as these actions are irreversible.
