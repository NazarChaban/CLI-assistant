# Contact Book CLI

This project provides a simple command-line interface (CLI) for managing a contact book. Users can add new contacts, change existing contact's phone numbers, find a specific contact's phone number, and display all contacts within the contact book.

## Features

- **Add new contact**: Users can add a new contact to the contact book with a name and phone number.
- **Change phone number**: Users can update the phone number for an existing contact.
- **Find phone number**: Users can retrieve the phone number associated with a given contact.
- **Show all contacts**: Users can view all the contacts and their phone numbers stored in the contact book.

## Error Handling

The program includes a decorator function `input_error` that wraps the main contact book functions to handle various exceptions such as incorrect input, non-existent users, duplicate users, and index errors. This ensures that the user receives a friendly error message instead of a Python stack trace if they make a mistake.

## Usage

To use the contact book, run the script and follow the CLI prompts:

- Type `hello` to receive a greeting message.
- To add a contact, type `add <name> <phone number>`.
- To change a contact's phone number, type `change <name> <new phone number>`.
- To find a contact's phone number, type `phone <name>`.
- To show all contacts, simply type `show all` or `show`.
- To exit the program, type one of the following commands: `good bye`, `close`, `exit`, or `.`.

## Commands

- `add`: Adds a new contact. Usage: `add John 1234567890`
- `change`: Changes the phone number of an existing contact. Usage: `change John 0987654321`
- `phone`: Retrieves the phone number for the given contact. Usage: `phone John`
- `show all` or `show`: Displays all contacts in the contact book. Usage: `show all` or `show`
- `hello`: Greets the user. Usage: `hello`
- `good bye`, `close`, `exit`, `.`: Exit the program.

## Main Function

The `main` function is the entry point of the program. It continuously reads user input and processes commands until exit commands are entered. The program parses the input and executes the corresponding command function from the `COMMANDS` dictionary.

### Contact Book Data Structure

The contact book data is stored in a dictionary (`FOLDER`) where the keys are contact names and values are their respective phone numbers.

---

Note: This README assumes that the intended audience has basic knowledge of how to run Python scripts from the command line.