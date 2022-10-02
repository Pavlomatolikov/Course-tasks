import re
import pickle
import sys


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
def add_contact(**kwargs):
    name = kwargs['name']
    phone = kwargs['phone']
    if not contact_list.get(name):
        contact_list[name] = phone
        return f'Phone {phone} was added for {name}'
    else:
        while True:
            raw_answer = input(
                f"Contact {name} already exists with phone {contact_list[kwargs['name']]}. Do you want to overwrite? Y/N: ")
            match_command = re.search(r'(?i)\by|yes|n|no\b', raw_answer)
            if match_command.group() in ('y', 'yes'):
                return change_phone(name=name, phone=phone)
            elif match_command.group() in ('n', 'no'):
                name = input('Please enter new name: ')
                return add_contact(name=name, phone=phone)


@input_error
def change_phone(**kwargs):
    name = kwargs['name']
    if contact_list.get(name):
        phone = kwargs['phone']
        contact_list[name] = phone
        return f"{name}'s phone was changed to {phone}"
    else:
        raise ValueError("Such conatact is absent in the contact list")


@input_error
def show_phone(**kwargs):
    name = kwargs['name']
    if contact_list.get(name):
        return f"{name} has {contact_list[name]} phone number"
    else:
        raise ValueError("Such conatact is absent in the contact list")


@input_error
def show_contact_list(**kwargs):
    return '\n'.join([f'{name} {telephone}' for name, telephone in sorted(contact_list.items())])


@input_error
def parting(**kwargs):
    return "Good bye!"


@input_error
def empty_input(**kwargs):
    return f'At least one of the following commands should be entered: {", ".join(OPERATIONS.keys())}'


OPERATIONS = {
    'hello': greetings,
    'add': add_contact,
    'change': change_phone,
    'phone': show_phone,
    'show all': show_contact_list,
    'good bye': parting,
    'close': parting,
    'exit': parting
}
contact_list = {}  # name: phone


def main():
    read_contact_list()
    while True:
        result = handler(
            **input_parser(
                input("Please enter a command with parameters: ")
            )
        )
        print(result)
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
            keys = ('command', 'name', 'phone')
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
    command = params.pop('command')
    if params:
        return OPERATIONS.get(command, empty_input)(**params)
    else:
        return OPERATIONS.get(command, empty_input)()


def read_contact_list():
    global contact_list
    try:
        with open('contact_list.data', 'rb') as filehandle:
            # read the data as binary data stream
            contact_list = pickle.load(filehandle)
    except (FileNotFoundError, EOFError):
        file = open('contact_list.data', 'wb')
        file.close()


def write_contact_list():
    with open('contact_list.data', 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(contact_list, filehandle)


if __name__ == "__main__":
    main()
