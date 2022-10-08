from collections import UserDict
import re
import pickle


class AddressBook(UserDict):
    def add_record(self, **kwargs):
        name = kwargs['name']
        if name not in self.data:
            record = Record(**kwargs)
            self.data[record.name.value] = record
            return f'Phone {record.phones[0].value} was added for {record.name.value}'
        else:
            raise ValueError(
                f"User with name {name} is already in the Address book. Please enter another name.")

    def edit_record(self, **kwargs):
        name = kwargs['name']
        if name in self.data:
            command = kwargs['command']
            if command == 'add phone':
                return self.data[name].add_phone(**kwargs)
            elif command == 'remove phone':
                return self.data[name].remove_phone(**kwargs)
            elif command == 'change phone':
                return self.data[name].change_phone(**kwargs)
        else:
            raise ValueError(
                f"User with name {name} was not found in the Address book. Please enter another name.")


class Record:
    def __init__(self, **kwargs):
        name = kwargs['name']
        self.phones = []
        self.name = Name(name)
        self.add_phone(**kwargs)

    def add_phone(self, **kwargs):
        name = kwargs['name']
        phone = kwargs['phone']
        if phone not in [phone.value for phone in self.phones]:
            self.phones.append(Phone(phone))
            return f'Phone {phone} was added for {name}'
        else:
            raise ValueError(
                f"User with name {name} already has enterred number {phone}.")

    def remove_phone(self, **kwargs):
        name = kwargs['name']
        phone = kwargs['phone']
        for phone_object in self.phones:
            if phone_object.value == phone:
                self.phones.remove(phone_object)
                return f'Phone {phone} was removed from {name} contact'
        else:
            raise ValueError(
                f"User with name {name} doesn't have number {phone}.")

    def change_phone(self, **kwargs):
        name = kwargs['name']
        phone = kwargs['phone']
        new_phone = kwargs['new_phone']
        self.remove_phone(**kwargs)
        self.add_phone(name=name, phone=new_phone)
        return f'Phone {phone} was replaced by {new_phone} for {name} contact'


class Field:
    # Класс Field, который будет родительским для всех полей, в нем потом реализуем логику общую для всех полей.
    pass


class Name(Field):
    def __init__(self, name) -> None:
        self.value = name


class Phone(Field):
    def __init__(self, phone) -> None:
        self.value = phone


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as param:
            return f"Enter also contact {param} please for this command"
        except ValueError as e:
            return e.args[0]
        except Exception as e:
            write_contact_list()
            return e.args
    return inner


@input_error
def greetings(**kwargs):
    return 'How can I help you?'


@input_error
def show_phone(**kwargs):
    name = kwargs['name']
    if contact_list.get(name):
        return f"{name} has {contact_list[name]} phone number"
    else:
        raise ValueError("Such conatact is absent in the contact list")


@input_error
def show_contact_list(**kwargs):
    return '\n'.join([f'{name} {" ".join(phone.value for phone in record.phones)}' for name, record in sorted(contact_list.items())])


@input_error
def parting(**kwargs):
    return "Good bye!"


@input_error
def empty_input(**kwargs):
    return f'At least one of the following commands should be entered: {", ".join(OPERATIONS.keys())}'


contact_list = AddressBook()
OPERATIONS = {
    'hello': greetings,
    'add contact': contact_list.add_record,
    'add phone': contact_list.edit_record,
    'remove phone': contact_list.edit_record,
    'change phone': contact_list.edit_record,
    'phone': show_phone,
    'show all': show_contact_list,
    'good bye': parting,
    'close': parting,
    'exit': parting
}


def main():
    read_contact_list()
    while True:
        result = handler(
            **input_parser(
                input("Please enter a command with parameters: ")
            )
        )
        print(result)
        # print(contact_list)
        if result == "Good bye!":
            write_contact_list()
            break


@input_error
def input_parser(user_input) -> dict:
    if user_input:
        normalized_user_input = re.sub(" +", " ", user_input.strip())
        match_command = re.search(r'(?i)\b{}\b'.format(
            r"\b|\b".join(OPERATIONS)), normalized_user_input)
        if match_command:
            keys = ('command', 'name', 'phone', 'new_phone')
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
    if params.get('command') and len(params) > 1:
        return OPERATIONS.get(command, empty_input)(**params)
    else:
        return OPERATIONS.get(command, empty_input)()


def read_contact_list():
    global contact_list
    try:
        with open('contact_list.data', 'rb') as filehandle:
            # read the data as binary data stream
            contact_list = pickle.load(filehandle)
            filehandle.close()
    except (FileNotFoundError, EOFError):
        file = open('contact_list.data', 'wb')
        file.close()


def write_contact_list():
    with open('contact_list.data', 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(contact_list, filehandle)


if __name__ == "__main__":
    main()
