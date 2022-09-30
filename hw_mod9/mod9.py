import re
import pickle


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (AttributeError, TypeError):
            print(
                'At least one of the following commands should be entered: ')
            for key in OPERATIONS:
                print(key)
            return None
        except KeyError as param:
            print(
                f"Enter also contact {param} please for {kwargs['command']} command")
    return inner


def greetings(**kwargs):
    print('How can I help you?')


@input_error
def add_contact(**kwargs):
    name = kwargs['name']
    phone = kwargs['phone']
    if not contact_list.get(name):
        contact_list[name] = phone
    else:
        while True:
            raw_answer = input(
                f"Contact {name} already exists with phone {contact_list[kwargs['name']]}. Do you want to overwrite? Y/N: ")
            match_command = re.search(r'(?i)\by|yes|n|no\b', raw_answer)
            if match_command.group() in ('y', 'yes'):
                # contact_list[name] = phone
                change_phone(name=name, phone=phone)
                break
            elif match_command.group() in ('n', 'no'):
                name = input('Please enter new name: ')
                add_contact(name=name, phone=phone)
                break


# @input_error
def change_phone(**kwargs):
    name = kwargs['name']
    phone = kwargs['phone']
    if contact_list[name]:
        contact_list[name] = phone


def show_phone():
    pass


def show_contact_list():
    pass


def parting():
    pass


OPERATIONS = {
    'hello': greetings,
    'add': add_contact,
    'change': change_phone,
    'phone': show_phone,
    'show all': show_contact_list,
    'good bye': parting
}
contact_list = {}  # name: phone


""""hello", отвечает в консоль "How can I help you?"
"add ...". По этой команде бот сохраняет в памяти (в словаре например) новый контакт. Вместо ... пользователь вводит имя и номер телефона, обязательно через пробел.
"change ..." По этой команде бот сохраняет в памяти новый номер телефона для существующего контакта. Вместо ... пользователь вводит имя и номер телефона, обязательно через пробел.
"phone ...." По этой команде бот выводит в консоль номер телефона для указанного контакта. Вместо ... пользователь вводит имя контакта, чей номер нужно показать.
"show all". По этой команде бот выводит все сохраненные контакты с номерами телефонов в консоль.
"good bye", "close", "exit" по любой из этих команд бот завершает свою роботу после того, как выведет в консоль "Good bye!"."""


def main():
    while True:
        try:
            handler(**input_parser(
                input("Please enter a command with parameters: ")))
            # print(contact_list)
        except ZeroDivisionError:  # (AttributeError, TypeError):
            print("Let's try again.")
            continue
    # read_contact_list()
    # print(contact_list)
    # write_contact_list()


@input_error
def input_parser(user_input) -> dict:
    normalized_user_input = re.sub(" +", " ", user_input.strip())
    match_command = re.search(r'(?i)\b{}\b'.format(
        "|".join(OPERATIONS)), normalized_user_input)
    input_list = [match_command.group()]
    params = normalized_user_input[match_command.end()+1::].split(' ')
    keys = ('command', 'name', 'phone')
    input_list.extend(params)
    # print(input_list)
    return {x: y for x, y in zip(keys, input_list)}


@input_error
def handler(**kwargs):
    return OPERATIONS[kwargs['command']](**kwargs)


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


# i_list = ['add', 'Name']
# comand, *name, phone = i_list
# print(comand, name, phone)
# b = " ".join(name)
# print(comand, b, phone)
# # a = {x: y for x, y in (comand, b, phone)}
# # print(a)
