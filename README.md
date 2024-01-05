# CLI phone book

This is a Command Line Interface (CLI) Address Book application written in Python. It allows users to manage contact information, including names, phone numbers, and birthdays. The application provides various commands to add, find, and manage contacts as well as to save and load the address book data from a file.

## Features

- **Add new contacts** with multiple phone numbers and an optional birthday.
- **Find a contact** and display all related information.
- **Find all contacts matching** a particular pattern in their names or phone numbers.
- **Delete a contact** and all associated data.
- **Save** the current state of the address book to a file.
- **Load** the address book data from a file.
- **Display all contacts** in the address book.
- **Display contacts** in paginated format, with a custom number of contacts **per page**.
- **Add a phone number** to an existing contact.
- **Remove a phone number** from an existing contact.
- **Edit an existing phone number** of a contact.
- **Set or update a birthday** for a contact.
- **Calculate the number** of days until a contact's next birthday.

## Installation

To use the Address Book application, you need to have Python installed on your system. If you don't have Python installed, download and install it from the [official Python website](https://www.python.org/downloads/).

Once Python is installed, clone this repository to your local machine:

## Usage
To start the application, run the following command in your terminal:
```sh
python address_book.py
```
Once the application is running, you will be able to use the following commands:

`add` <name> <phone1> <phone2> ... [birthday]: Add a new contact.
`find` <name>: Find and display a contact's information.
`find matches` <pattern>: Find and display all contacts that match the pattern.
`delete` <name>: Delete a contact.
`save`: Save the address book to a file.
`load`: Load the address book from a file.
`show all`: Display all contacts.
`show` <n>: Display contacts in pages, n contacts per page.
`add phone` <name> <phone>: Add a phone number to a contact.
`remove phone` <name> <phone>: Remove a phone number from a contact.
`edit phone` <name> <old_phone> <new_phone>: Edit a contact's phone number.
`find phone` <name> <phone>: Find and display a specific phone number.
`add birthday` <name> <birthday>: Add or update a contact's birthday.
`days to birthday` <name>: Show the number of days until a contact's next birthday.
To exit the application, type `good bye`, `close`, `exit`, or `.`.

## Contributing
Contributions to YOUR_PROJECT_NAME are welcome! Feel free to submit pull requests or open issues to improve the functionality or fix issues within the application.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
