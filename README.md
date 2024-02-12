# Email Management CLI

This is a command-line interface (CLI) tool for managing and performing actions on emails. The tool is built using Python and asyncio, leveraging the Prisma library for database interactions.

## Installation

To install the dependencies, clone the repository and navigate to the project directory:

```bash python -m venv venv```
```bash source venv/bin/activate```
```bash pip install -r requirements.txt```

## Features

### Email Collection

To collect emails, use the following command:

```bash
python script_name.py collect --count <number_of_emails_to_fetch>
```

This command fetches a specified number of emails and stores them in the database.

### Email Actions

Perform various actions on the collected emails using the `action` command:

```bash
python script_name.py action
```

The tool prompts you to choose a rule to filter emails. After selecting a rule, you can choose from the following actions:

1. **Read**: Mark selected emails as read.
2. **Unread**: Mark selected emails as unread.
3. **Move**: Move selected emails to a specific folder.

### Rules and Filters

You can customize rules and filters for email actions. Modify the `lib.filters.py` file to define rules based on your criteria.

### Running the CLI

To run the CLI, execute the script:

```bash
python script_name.py
```

## Dependencies

Make sure to install the required dependencies before running the script:

```bash
pip install click asyncio prisma
```

## Disclaimer

This tool is designed for managing emails programmatically. Ensure that you understand the actions being performed, especially when moving emails or marking them as read/unread, as these actions are irreversible.

## Contributions

Feel free to contribute to the project by submitting bug reports, feature requests, or pull requests. Your feedback is valuable in enhancing the functionality and usability of the tool.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
