import re
from collections import UserDict

class Field:
    def __init__(self, value = ''):
        self.value = value
    def __repr__(self):
        return self.value
    def __eq__(self, other):
        return self.value == other
        
class Phone(Field):
    pass

class Name(Field):
    pass
    
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    def __repr__(self):
        return '\n'.join(map(lambda p: p.value, self.phones))
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    def remove_phone(self, phone):
        self.phones.remove(Phone(phone))
    def change_phone(self, oldphone, newphone):
        try:
            index = self.phones.index(Phone(oldphone))
        except ValueError:
            raise ValueError('phone not found') 
        self.phones[index] = Phone(newphone)

class AddressBook(UserDict):
    def add_record(self, name, phone):
        if name in self.data: 
            self.data[name].add_phone(phone)
            return f'new phone for user {name} added'
        else:
            self.data[name] = Record(name)
            self.data[name].add_phone(phone)
            return f'user {name} added'
    def change_record(self, name, oldphone, newphone):
        try:
            self.data[name].change_phone(oldphone, newphone)
            return 'phone changed'
        except KeyError:
            return f'contact {name} not found'

    def get_record(self, name):
        return self.data.get(name) or 'no records'

    def remove_record(self, name):
        return self.data.pop(name)

class User:
    user_id = 1
    def __init__(self, name):
        self.name = name
        self.address_book = AddressBook(dict())
        self.id = User.user_id
        User.user_id += 1

def input_error(func):
    def inner(string):
        try:
            ret = func(string)
            return ret
        except (KeyError, ValueError, IndexError) as err:
            return err
    return inner

@input_error
def hello(args_string):
    if args_string:
        raise ValueError('incorrect args\nuse "hello" without args')
    return 'How can I help you?'

@input_error
def add(args_string):
    args = args_string.split()

    if len(args) != 2:
        raise ValueError('incorrect args\nplease enter: add <name> <phone>')

    if not (isname(args[0]) and isphone(args[1])):
        raise ValueError('incorrect name or phone')

    return user.address_book.add_record(args[0], sanitize_phone_number(args[1]))

@input_error
def change(args_string):
    args = args_string.split()

    if len(args) != 3:
        raise ValueError('incorrect args\nplease enter: change <name> <old phone> <new phone>')

    if not (isname(args[0]) and isphone(args[1]) and isphone(args[2])):
        raise ValueError('incorrect name or phone')

    return user.address_book.change_record(args[0], sanitize_phone_number(args[1]), sanitize_phone_number(args[2]))

@input_error
def phone(args_string):
    if len(args_string.split()) != 1:
        raise ValueError('please enter a name')

    name = args_string.strip()

    if not isname(name):
        raise ValueError('incorrect name')

    return user.address_book.get_record(name)

@input_error
def showall(args_string):
    if args_string:
        raise ValueError('incorrect args\nuse "show all" without args')
    str = ''
    for name in user.address_book:
        str += f'{name}:\n{user.address_book.get_record(name)}\n'
    return str.rstrip('\n') or 'no records'

@input_error
def quit(args_string):
    if args_string:
        raise ValueError('incorrect args\nuse "exit" without args')
    return 'Good bye!'

def check_input(string):
    return not re.search(r'[^A-Za-z0-9\.\,\s\+]', string)

def isname(string):
    return not re.search(r'[^A-Za-z]', string)

def sanitize_phone_number(phone):
    return phone.replace(' ','').replace('(','').replace(')','').replace('+','').replace('-','')

def isphone(string):
    return not re.search(r'[^0-9]', sanitize_phone_number(string))

@input_error
def parse_input(string):

    if not check_input(string):
        raise ValueError('"'+string+'" not a valid command\nunsupported chars') 
    result = re.sub(r'[\s\,]+', ' ', string.strip())

    for command in FUNC_DICT:
        if result.lower().startswith(command):
            return (command, result[len(command):])

    raise ValueError(result.split()[0]+' not a valid command')
    
def get_record(name):
    return USERS_DICT.get(name) or f'user not found: {name}'

def main():
    while True:
        user_input = input('>>> ')
        if user_input ==  '.':
            exit()
        command = parse_input(user_input)

        if isinstance(command, (str, Exception)):
            print(command)
        elif isinstance(command, tuple):
            result = FUNC_DICT[command[0]](command[1])
            print(result)
            if result == 'Good bye!':
                exit()

FUNC_DICT={'hello': hello, 'add': add, 'change': change, 'phone': phone, 'show all': showall, 'exit': quit, 'good bye': quit, 'close': quit}
USERS_DICT=dict()
user = User('defaultuser')

if __name__ == '__main__':
    main()