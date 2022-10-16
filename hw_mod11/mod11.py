from collections import UserDict
from datetime import datetime
import re
import pickle
from tabnanny import check


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as param:
            return f"Enter also contact {param} please for this command"
        except TypeError as e:
            return e.args[0]
        except ValueError as e:
            return e.args[0]
        except AttributeError as e:
            return f"This contact doesn't have saved birthday."
        except Exception as e:
            write_contact_book()
            return e.args
    return inner


class AddressBook(UserDict):
    def add_record(self, name, phone=None, additional1=None, **kwargs):
        if phone and additional1 and name not in self.data:
            record = Record(name=name, phone=phone, birthday=additional1)
            self.data[record.name.value] = record
            return f'Phone {record.phones[0].value} and birthday {record.birthday.value} was added for {record.name.value}'
        elif phone and not additional1 and name not in self.data:
            record = Record(name=name, phone=phone)
            self.data[record.name.value] = record
            return f'Phone {record.phones[0].value} was added for {record.name.value}'
        elif not phone and name not in self.data:
            record = Record(name=name)
            self.data[record.name.value] = record
            return f'Contact {record.name.value} was added without phone, since it was not enterred.'
        else:
            raise ValueError(
                f"User with name {name} is already in the Address book. Please enter another name.")

    def edit_record(self, command, name, phone=None, additional1=None, ** kwargs):
        if name in self.data:
            if command == 'add phone':
                return self.data[name].add_phone(name=name, phone=phone)
            elif command == 'remove phone':
                return self.data[name].remove_phone(name=name, phone=phone)
            elif command == 'change phone':
                return self.data[name].change_phone(name=name, phone=phone, additional1=additional1)
        else:
            raise ValueError(
                f"User with name {name} was not found in the Address book. Please enter another name.")

    def get_info(self, command, name, **kwargs):
        if name in self.data:
            if command == 'days to birthday':
                return self.data[name].days_to_birthday()

    def iterator(self, paginator, page_size, **kwargs):
        page = {}
        for i in range(int(page_size)):
            try:
                page.update(dict((x, y) for x, y in (next(paginator), )))
            except StopIteration:
                return page
        return page


class Record:
    def __init__(self, name, phone=None, birthday=None, **kwargs):
        self.phones = []
        self.name = Name(name=name)
        if birthday:
            self.birthday = Birthday(birthday=birthday)
        if phone:
            self.add_phone(name=name, phone=phone)

    def add_phone(self, name, phone=None, **kwargs):
        if phone and phone not in [phone.value for phone in self.phones]:
            self.phones.append(Phone(phone=phone))
            return f'Phone {phone} was added for {name}'
        if not phone:
            return f'Phone was not added since it was not enterred.'
        else:
            raise ValueError(
                f"User with name {name} already has enterred number {phone}.")

    def remove_phone(self, name, phone=None, **kwargs):
        for phone_object in self.phones:
            if phone_object.value == phone:
                self.phones.remove(phone_object)
                return f'Phone {phone} was removed from {name} contact'
        else:
            raise ValueError(
                f"User with name {name} doesn't have number {phone}.")

    def change_phone(self, name, phone=None, additional1=None, **kwargs):
        a = self.remove_phone(name=name, phone=phone)
        b = self.add_phone(name=name, phone=additional1)
        return a, b

    def days_to_birthday(self):
        today = datetime.now().date()
        current_year = today.year
        birthday = self.birthday.value.date().replace(year=current_year)
        delta = birthday - today
        return f"{delta.days} days to {self.name.value} birthday."


class Field:
    # Класс Field, который будет родительским для всех полей, в нем потом реализуем логику общую для всех полей.
    _pattern = ".+"

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if self._check(new_value):
            self.__value = new_value
        else:
            raise TypeError(
                f"Incorrect {type(self).__name__} value")

    @input_error
    def _check(self, value):
        if re.fullmatch(self._pattern, value):
            return True


class Name(Field):
    def __init__(self, name) -> None:
        self.value = name


class Phone(Field):
    def __init__(self, phone) -> None:
        self.value = phone
    _pattern = "\+?[\d()-]+"


class Birthday(Field):
    def __init__(self, birthday) -> None:
        try:
            self.value = datetime.strptime(birthday, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Birthday should match format 'YYYY-MM-DD'.")

    def _check(self, value):
        target_date = value
        delta = datetime.now() - target_date
        if delta.days > 0:
            return True


@input_error
def greetings(**kwargs):
    return 'How can I help you?'


@input_error
def show_phone(**kwargs):
    name = kwargs['name']
    if name in contact_book:
        return f"{name} has {' '.join(phone.value for phone in contact_book[name].phones)} phone number/s"
    raise ValueError("Such conatact is absent in the contact list")


@input_error
def show_contact_book(**kwargs):
    raw_answer = input(f"Do you want to see full Address book? Y/N: ")
    match_command = re.search(r'(?i)\by|yes|n|no\b', raw_answer)
    if match_command and match_command.group() in ('y', 'yes'):
        return '\n'.join([f'{name} {", ".join(phone.value for phone in record.phones)} {record.birthday.value.date() if hasattr(record, "birthday") else ""}' for name, record in sorted(contact_book.items())])
    elif not match_command or match_command.group() not in ('y', 'yes'):
        answer = input(f"Please enter amount of records per page: ")
        paginator = iter(contact_book.data.items())
        while True:
            page = contact_book.iterator(paginator, int(answer))
            if page:
                print('\n'.join(
                    [f'{name} {", ".join(phone.value for phone in record.phones)} {record.birthday.value.date() if hasattr(record, "birthday") else ""}' for name, record in sorted(page.items())]))
            else:
                return "Pagination if finished"
            raw_answer = input(f"Do you want to see next page? Y/N: ")
            match_command = re.search(r'(?i)\by|yes|n|no\b', raw_answer)
            if not match_command or match_command.group() not in ('y', 'yes'):
                return "Pagination if finished"


@input_error
def parting(**kwargs):
    return "Good bye!"


@input_error
def empty_input(**kwargs):
    return f'At least one of the following commands should be entered: {", ".join(OPERATIONS.keys())}'


contact_book = AddressBook()


OPERATIONS = {
    'hello': greetings,
    'add contact': contact_book.add_record,
    'add phone': contact_book.edit_record,
    'remove phone': contact_book.edit_record,
    'change phone': contact_book.edit_record,
    'phone': show_phone,
    'show all': show_contact_book,
    'days to birthday': contact_book.get_info,
    'good bye': parting,
    'close': parting,
    'exit': parting
}


def main():
    read_contact_book()
    while True:
        result = handler(
            **input_parser(
                input("Please enter a command with parameters: ")
            )
        )
        if isinstance(result, str):
            print(result)
        else:
            for i in result:
                print(i)
        if result == "Good bye!":
            write_contact_book()
            break


@input_error
def input_parser(user_input) -> dict:
    if user_input:
        normalized_user_input = re.sub(" +", " ", user_input.strip())
        match_command = re.search(r'(?i)\b{}\b'.format(
            r"\b|\b".join(OPERATIONS)), normalized_user_input)
        if match_command:
            keys = ('command', 'name', 'phone', 'additional1')
            input_list = [match_command.group()]
            if len(user_input) != match_command.end():
                params = normalized_user_input[match_command.end(
                )+1::].split(' ')
                input_list.extend(params)
            return {x: y for x, y in zip(keys, input_list)}
    return {'command': 'empty'}


@input_error
def handler(**kwargs):
    params = kwargs
    command = params.get('command')
    if 'command' in params and len(params) > 1:
        return OPERATIONS.get(command, empty_input)(**params)
    return OPERATIONS.get(command, empty_input)()


def read_contact_book():
    global contact_book
    try:
        with open('contact_book.data', 'rb') as filehandle:
            # read the data as binary data stream
            contact_book.update(pickle.load(filehandle))
    except (FileNotFoundError, EOFError):
        file = open('contact_book.data', 'wb')
        file.close()


def write_contact_book():
    with open('contact_book.data', 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(contact_book, filehandle)


if __name__ == "__main__":
    main()
