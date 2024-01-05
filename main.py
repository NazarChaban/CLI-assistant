from collections import UserDict
from datetime import datetime
from pickle import dump, load
import re


class Connection:
    def __init__(self, adr_book):
        self.__adr_book = adr_book

    def __enter__(self):
        msg = self.__adr_book.load_data()
        print(f'Connection: {msg}')

    def __exit__(self, exc_type, exc_value, traceback):
        msg = self.__adr_book.save_data()
        print(f'Connection: {msg}')


class Field:
    def __init__(self, value):
        if self.validate(value):
            self.__value = value

    def validate(slef, new_value):
        return True

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if self.validate(new_value):
            self.__value = new_value

    def __str__(self):
        return str(self.__value)


class Name(Field):
    pass


class Birthday(Field):
    def validate(slef, new_birth):
        if new_birth is None:
            return True
        elif not all([len(new_birth) == 10,
                      isinstance(new_birth, str)]):
            raise ValueError('Wrong date format, should be dd.mm.yyyy')
        return True


class Phone(Field):
    def validate(slef, new_phone):
        if not all([len(new_phone) == 10,
                    new_phone.isdecimal()]):
            raise ValueError('Wrong phone number format, should be 10 digits')
        return True


class Record:
    def __init__(self, name, *phones, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(i) for i in phones] if phones else []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        if phone not in map(lambda x: x.value, self.phones):
            self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for el in self.phones:
            if el.value == phone:
                self.phones.remove(el)

    def edit_phone(self, old, new):
        temp = {p.value: p for p in self.phones}
        if old in temp.keys():
            old_ind = self.phones.index(temp[old])
            self.phones[old_ind].value = new
        else:
            raise ValueError('No such phone number')

    def find_phone(self, phone):
        temp = {p.value: p for p in self.phones}
        if phone in temp.keys():
            return temp[phone]
        return None

    def add_birthday(self, birthday):
        if self.birthday.value is None:
            self.birthday.value = birthday
        else:
            raise ValueError('Birthday is already set')

    def days_to_birthday(self):
        if self.birthday.value is not None:
            cur_date = datetime.now().date()
            try:
                cur_birthday = datetime.strptime(self.birthday.value,
                                                 '%d.%m.%Y').date()
            except ValueError('Wrong date format, should be dd.mm.yyyy'):
                return None
            next_birth = cur_birthday.replace(year=cur_date.year)
            if next_birth < cur_date:
                next_birth = next_birth.replace(year=cur_date.year + 1)
            return (next_birth - cur_date).days
        return None

    def __str__(self):
        if self.birthday.value is None:
            return f"Contact name: {self.name.value}; " \
                   f"phones: {', '.join(p.value for p in self.phones)}."

        return f"Contact name: {self.name.value}; " \
               f"phones: {', '.join(p.value for p in self.phones)}; " \
               f"birthday: {self.birthday.value}."


class AddressBook(UserDict):
    def add_record(self, user):
        if user.name.value in self.data.keys():
            raise ValueError('User already exists')
        self.data[user.name.value] = user

    def find_user(self, name):
        return self.data.get(name, None)

    def find_mathes(self, info):
        if info.isdecimal():
            temp = set()
            for value in self.data.values():
                for phone in value.phones:
                    if info in phone.value:
                        temp.add(str(value))
            return [i for i in temp]
        elif info.isalpha():
            return [str(p) for p in self.data.values() if info in p.name.value]
        else:
            raise ValueError('Wrong input format')

    def delete(self, name):
        if self.data.get(name) is not None:
            del self.data[name]

    def show_all(self):
        return '\n'.join(str(record) for record in self.data.values())

    def iterator(self, n):
        start = 0
        step = n
        end = len(self.data)
        while start < end:
            temp = list(self.data.values())[start:step]
            yield [str(i) for i in temp]
            start += n
            step += n

    def save_data(self):
        with open('data.bin', 'wb') as fd:
            dump(self.data, fd)
        return 'Data saved'

    def load_data(self):
        try:
            with open('data.bin', 'rb') as fd:
                self.data = load(fd)
            return 'Data loaded'
        except Exception:
            self.data = dict()
            return 'No data to load'


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)
    return wrapper


@input_error
def add_user_handler(book, name, phones, birthday=None):
    record = Record(name, *phones, birthday=birthday)
    book.add_record(record)
    return f'User {name} was added!'


@input_error
def find_user_handler(book, name):
    record = book.find_user(name)
    if record is None:
        raise KeyError(f'User with name {name} not found')
    return str(record)


@input_error
def find_matches_handler(book, pattern):
    return '\n'.join(book.find_mathes(pattern))


@input_error
def delete_user_handler(book, name):
    book.delete(name)
    return f'User {name} was deleted!'


@input_error
def save_data_handler(book):
    return book.save_data()


@input_error
def load_data_handler(book):
    return book.load_data()


@input_error
def show_all_handler(book):
    return book.show_all()


page_iterator = None


@input_error
def show_page_handler(book, n):
    n = int(n)
    if n == 0:
        raise ValueError('n should be greater than 0')

    if n >= len(book.data):
        return book.show_all()

    global page_iterator
    if not page_iterator:
        page_iterator = book.iterator(n)
    try:
        return '\n'.join(next(page_iterator))
    except StopIteration:
        page_iterator = None
        return 'End of address book.'


@input_error
def add_phone_handler(book, name, phone):
    record = book.find_user(name)
    if record is None:
        raise KeyError(f'User with name {name} not found')
    record.add_phone(phone)
    return f'Phone {phone} was added to user {name}.'


@input_error
def remove_phone_handler(book, name, phone):
    record = book.find_user(name)
    if record is None:
        raise KeyError(f'User with name {name} not found')
    record.remove_phone(phone)
    return f'Phone {phone} was removed from user {name}.'


@input_error
def edit_phone_handler(book, name, old_phone, new_phone):
    record = book.find_user(name)
    if record is None:
        raise KeyError(f'User with name {name} not found')
    record.edit_phone(old_phone, new_phone)
    return 'Phone number changed!'


@input_error
def find_phone_handler(book, name, phone):
    record = book.find_user(name)
    if record is None:
        raise KeyError(f'User with name {name} not found')
    if record.find_phone(phone) is not None:
        return phone
    else:
        return 'Phone number not found'


@input_error
def add_birthday_handler(book, name, birthday):
    record = book.find_user(name)
    if record is None:
        raise KeyError(f'User with name {name} not found')
    record.add_birthday(birthday)
    return f'Birthday {birthday} was added to user {name}.'


@input_error
def days_to_birthday_handler(book, name):
    record = book.find_user(name)
    if record is None:
        raise KeyError(f'User with name {name} not found')
    days = record.days_to_birthday()
    if days is not None:
        return f'{days} days to the birthday of user {name}.'
    else:
        return 'Birthday not set for user {name}.'


def parse_input(user_input):
    patterns = {
        'add': r'^add\s+(?P<name>\w+)\s+(?P<phones>(?:\d{10}\s*)*)'\
               r'(?P<birthday>(?:\d{2}\.\d{2}\.\d{4})?)?$',
        'find': r'^find\s+(?P<name>\w+)$',
        'find matches': r'^find matches\s+(?P<pattern>\w+)$',
        'delete': r'^delete\s+(?P<name>\w+)$',
        'save': r'^save$',
        'load': r'^load$',
        'show all': r'^show all$',
        'show': r'^show\s+(?P<n>\d+)$',
        'add phone': r'^add phone\s+(?P<name>\w+)\s+(?P<phone>\d{10})$',
        'remove phone': r'^remove phone\s+(?P<name>\w+)\s+(?P<phone>\d{10})$',
        'edit phone': r'^edit phone\s+(?P<name>\w+)\s+(?P<old_phone>\d{10})'\
                      r'\s+(?P<new_phone>\d{10})$',
        'find phone': r'^find phone\s+(?P<name>\w+)\s+(?P<phone>\d{10})$',
        'add birthday': r'^add birthday\s+(?P<name>\w+)\s+'\
                        r'(?P<birthday>\d{2}\.\d{2}\.\d{4})$',
        'days to birthday': r'^days to birthday\s+(?P<name>\w+)$',
    }
    for command, pattern in patterns.items():
        match = re.match(pattern, user_input.strip())
        if match:
            if command == 'add':
                arg = match.groupdict()
                arg['phones'] = arg['phones'].split()
                arg['birthday'] = arg['birthday'] if arg['birthday'] else None
                return command, arg
            return command, match.groupdict()
    raise ValueError('Invalid input format')


COMMANDS = {
    'add': add_user_handler,
    'find': find_user_handler,
    'find matches': find_matches_handler,
    'delete': delete_user_handler,
    'save': save_data_handler,
    'load': load_data_handler,
    'show all': show_all_handler,
    'show': show_page_handler,
    'add phone': add_phone_handler,
    'remove phone': remove_phone_handler,
    'edit phone': edit_phone_handler,
    'find phone': find_phone_handler,
    'add birthday': add_birthday_handler,
    'days to birthday': days_to_birthday_handler,
}


def help():
    com = {
        'add [name] [phones] [birthday]': 'add new record to address book',
        'find [name]': 'find record in address book by name',
        'find matches [info]': 'find record in address book by matched info',
        'delete [name]': 'delete record from address book by name',
        'save': 'save data to file',
        'load': 'load data from file',
        'show [all/n]': 'show all records or n records per page',
        'add phone [name]': 'add new phone number to record',
        'remove phone [name] [phone]': 'remove phone number from record',
        'edit phone [old] [new]': 'edit phone number in record',
        'find phone [name] [phone]': 'return phone from record if it exists',
        'add birthday [name] [date]': 'add birthday to record',
        'days to birthday [name]': 'return days to birthday if it exists'
    }
    print(f'{'Help':-^78}')
    for k, v in com.items():
        print(f'|{k:<31}|{v:<44}|')
    print(f'{"":-<78}')


def main():
    book = AddressBook()
    with Connection(book):
        while True:
            user_input = input('>>> ').strip().lower()

            if user_input in ('hello',):
                print('How can I help you?')
                continue

            if user_input == 'help':
                help()

            if user_input in ('good bye', 'close', 'exit', '.'):
                print('Good bye!')
                break

            try:
                command, args = parse_input(user_input)
                if command not in COMMANDS:
                    raise ValueError('Wrong command! Try again.')

                handler = COMMANDS[command]
                print(handler(book, **args))
            except Exception as e:
                print(e)


if __name__ == '__main__':
    main()
