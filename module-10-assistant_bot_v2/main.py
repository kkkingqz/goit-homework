from hashlib import new
import re
from collections import UserDict, UserString, defaultdict

class Field(UserString):
    def __init__(self, seq: object) -> None:
        super().__init__(seq)
        self.value = self.data #создаем value следуя букве ТЗ. так то тут это не нужно
    def __format__(self, __format_spec: str) -> str:
        return str.__format__(self.data, __format_spec)

class Phone(Field):
    pass

class Name(Field):
    pass

class EMail(Field):
    pass

class Record():
    DEFAULT_FIELDS = {'phone': Phone, 'email': EMail}

    def __init__(self, name, field_type='', values=''):
        self.name = Name(name)
        self.data = defaultdict(list)

        self.phones = self.data['phone']
        self.emails = self.data['email']

        if field_type and values:
            self.add_field(field_type, values)
   
    def add_field(self, field_type, values):
        self.data[field_type].extend(map(lambda v: Record.DEFAULT_FIELDS.get(field_type, Field)(v), values))
        return f'add {field_type} for contact: {self.name}'

    def change_field(self, field_type, oldvalue, newvalue):#oldphone, newphone):
        try:
            index = self.data[field_type].index(Record.DEFAULT_FIELDS.get(field_type, Field)(oldvalue))
        except ValueError:
            raise ValueError(f'{field_type} not found') 
        self.data[field_type][index] = Record.DEFAULT_FIELDS.get(field_type, Field)(newvalue)
        return f'{field_type} change'

    def remove_field(self, field_type, value):
        try:
            index = self.data[field_type].index(Record.DEFAULT_FIELDS.get(field_type, Field)(value))
        except ValueError:
            raise ValueError(f'{field_type} not found') 
        self.data[field_type].pop(index)
        return f'{field_type} removed'

    def remove_field_type(self, field_type):
        if not field_type in self.data:
            raise ValueError(f'{field_type} not found')
        self.data.pop(field_type)
        return f'{field_type}s removed'

class AddressBook(UserDict):
    def add_record(self, name, field_type='', *values):
        if name not in self.data:
            self.data[name] = Record(name, field_type, values)
            return f'contact {name} created'

        return self.data[name].add_field(field_type, values)

    def remove_record(self, name):
        if self.data.pop(name):
            return f'contact {name} removed'
        else:
            return f'contact {name} not found'

    def change_record_field(self, name, field, oldvalue, newvalue):
        try:
            return self.data[name].change_field(field, oldvalue, newvalue)
        except KeyError:
            raise KeyError(f'contact {name} not found')

    def show(self, name, field='', maxlen=80):
        result = '*'*maxlen+'\n'
        result += ('|  {:^'+str(maxlen-6)+'}  |\n').format(self.data[name].name.upper())
        result += '*'*maxlen+'\n'
        for count, phone in enumerate(self.data[name].phones):
            result += ('|  {:^10}  |  {:^'+str(maxlen-21)+'}  |\n').format('phone '+str(count+1), phone)
            result += '-'*maxlen+'\n'
        result = '\n'.join(result.split('\n')[:-2])
        result += '\n'+'*'*maxlen+''
        return result

    def showall(self, maxlen=80):
        result = ''
        for contact in self.data:
            result += self.show(contact, maxlen)+'\n'
        return result




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

    if len(args) < 2:
        raise ValueError('incorrect args\nplease enter: add <name> <phone>')

    #if not (isname(args[0]) and isphone(args[1])):
    #    raise ValueError('incorrect name or phone')
    #print(args[1:0])
    return contacts.add_record(args[0], *args[1:])#*map(lambda p: p, args[1:]))#[*map(lambda p: sanitize_phone_number(p), args[1:])])

@input_error
def change(args_string):
    args = args_string.split()

    if len(args) != 3:
        raise ValueError('incorrect args\nplease enter: change <name> <old phone> <new phone>')

    if not (isname(args[0]) and isphone(args[1]) and isphone(args[2])):
        raise ValueError('incorrect name or phone')

    return contacts.change_record_phone(args[0], sanitize_phone_number(args[1]), sanitize_phone_number(args[2]))

@input_error
def phone(args_string):
    if len(args_string.split()) != 1:
        raise ValueError('please enter a name')

    name = args_string.strip()

    if not isname(name):
        raise ValueError('incorrect name')

    return contacts.show(name)

@input_error
def showall(args_string):
    if args_string:
        raise ValueError('incorrect args\nuse "show all" without args')

    return contacts.showall()

@input_error
def quit(args_string):
    if args_string:
        raise ValueError('incorrect args\nuse "exit" without args')
    return 'Good bye!'

def check_input(string):
    return True
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
contacts = AddressBook(dict())

if __name__ == '__main__':
    main()