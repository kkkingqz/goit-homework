import re
from collections import UserDict, defaultdict
from datetime import date, datetime

try:
    import dateutil.parser as Dateparse
except ModuleNotFoundError:
    print('Please install python module "dateutil". pip install python-dateutil')
    class Dateparse():
        class _parser():
            class ParserError(Exception):
                pass
        def parse(string):
            try:
                return datetime.strptime(string, '%Y-%m-%d')
            except ValueError:
                raise Dateparse._parser.ParserError


class Field():
    def __init__(self, seq: object) -> None:
        self.__value = None
        self.value = seq

    def __format__(self, __format_spec: str) -> str:
        return str.__format__(self.value, __format_spec)

    def __str__(self) -> str:
        return self.__value

    def lower(self):
        return str.lower(self.__value)

    def upper(self):
        return str.upper(self.__value)
        
    @property
    def value(self):
        return self.__value
    @value.setter
    def value(self, string):
        self.__value = string

class Phone(Field):
    def sanitize_phone_number(self, string):
        return string.replace(' ','').replace('(','').replace(')','').replace('+','').replace('-','')       

    @property
    def value(self):
        return f'({self.__value[:3]}) {self.__value[3:]}'
    @value.setter
    def value(self, value):
        if not re.search(r'[^0-9]', self.sanitize_phone_number(value)):
            self.__value = self.sanitize_phone_number(value)
        else:
            raise ValueError('incorrect phone number')

class Name(Field):
    pass

class Birthday(Field):
    @property
    def birthday_current_year(self):
        return date(year=datetime.now().year, month=self.__value.month, day=self.__value.day)
    @property
    def birthday(self):
        return self.__value
    @property
    def value(self):
        return date.strftime(self.__value, '%Y-%m-%d')
    @value.setter
    def value(self, string):
        try:
            self.__value = Dateparse.parse(string).date()
        except Dateparse._parser.ParserError:
            raise ValueError('incorrect date format. enter yyyy-mm-dd')

class Record():

    def __init__(self, name, phones):
        self.name = Name(name)
        self.phones = list()
        self.birthday = None
        self.add_phones(phones)
    
    def add_phones(self, phones):
        self.phones.extend(map(lambda v: Phone(v), phones))
        return f'added phones for contact: {self.name}'

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return f'added birhday for contact: {self.name}'

    def change_phone(self, oldvalue, newvalue):
        index = self.phones.index(Phone(oldvalue))
        self.phones[index] = Phone(newvalue)
        return f'Phone change'

    def remove_phone(self, value):
        index = self.phones.index(Phone(value))
        self.phones.pop(index)
        return f'phone removed'

    def days_to_birthday(self):
        today = date.today()
        current_year_bd = self.birthday.birthday_current_year
        days = str((current_year_bd - today).days)
        return f'today is {today}. {self.name} birthday day in current year - {current_year_bd}\n{days} day(s)'

class AddressBook(UserDict):
    def add_record(self, name, *phones):
        if name not in self.data:
            self.data[name] = Record(name, phones)
            return f'contact {name} created'

        return self.data[name].add_phones(phones)

    def remove_record(self, name):
        self.data.pop(name)
        return f'contact {name} removed'

    def show(self, name):
        maxlen=80
        result = '*'*maxlen+'\n'
        result += ('|  {:^'+str(maxlen-6)+'}  |\n').format(self.data[name].name.upper())
        result += '*'*maxlen+'\n'
        
        for count, value in enumerate(self.data[name].phones):
            result += ('|  {:^10}  |  {:^'+str(maxlen-21)+'}  |\n').format(str(count+1), value)
            result += '-'*maxlen+'\n'
        result += ('|  {:^10}  |  {:^'+str(maxlen-21)+'}  |\n').format('birthday', self.data[name].birthday)

        result = '\n'.join(result.split('\n')[:-2])
        result += '\n'+'*'*maxlen+''
        return result

    def iterator(self, n):
        result = ''
        for i, key in enumerate(self.keys()):
            result += self.show(key)+'\n'
            if (i+1) % n == 0:
                yield result
                result = ''
        if result:
            yield result

    def showall(self):
        result = ''
        for contact in self.data:
            result += self.show(contact)+'\n'
        return result

def input_error(func):
    def inner(string):
        try:
            ret = func(string)
            return ret
        except (KeyError, ValueError, IndexError) as err:
            if func.__name__ in ('change', 'phone', 'show', 'remove', 'birthday'):
                return 'record not found'
            return err
    return inner

def processing_args(args_string, args_num_min, args_num_max, help_string=''):
    args = args_string.split()

    try:
        if args[0] == 'help':
            raise ValueError(help_string)
    except IndexError:
        pass

    if args_num_max == 0 and args:
        raise ValueError('incorrect args\nuse without args\n'+help_string)

    if not (args_num_min <= len(args) <= args_num_max):
        raise ValueError('incorrect number of arguments\n'+help_string)

    if len(args) > 0:
        if re.search(r'[^A-Za-z]', args[0]):
            raise ValueError('incorrect name')

    return args

@input_error
def hello(args_string):
    args = processing_args(args_string, 0, 0)
    return 'How can I help you?'

@input_error
def add(args_string):
    args = processing_args(args_string, 3, 99, 'use:\n   add <name> <phone> [<phone2>, ...]\n   add <name> birthday <birthday>')    
    if args[1] == 'birthday' and len(args) == 3:
        return contacts[args[0]].add_birthday(args[2]) 
    return contacts.add_record(*args)

@input_error
def change(args_string):
    args = processing_args(args_string, 3, 4, 'use:\n   change <name> phohe <old value> <new value>\n or \n   change <name> birthday <new value>')    
    if args[1] == 'phone':
        return contacts[args[0]].change_phone(args[2], args[3])
    elif args[1] == 'birthday':
        return contacts[args[0]].add_birhday(args[2])
    else:
        raise ValueError('incorrect')

@input_error
def phone(args_string):
    args = processing_args(args_string, 1, 1, 'use:\n   phone <name>')
    return contacts.show(args[0])

@input_error
def show(args_string):
    args = processing_args(args_string, 1, 1, 'use:\n   show <name>')
    return contacts.show(*args)

@input_error
def showall(args_string):
    args = processing_args(args_string, 0, 0)
    return contacts.showall()

@input_error
def remove(args_string):
    args = processing_args(args_string, 1, 1, 'use:\n   remove <name>\n   or\n   remove <name> <field type>\n   or\n   remove <name> <field type> <value>')

    return contacts.remove_record(args[0])

@input_error
def quit(args_string):
    args = processing_args(args_string, 0, 0)
    return 'Good bye!'

@input_error
def birthday(args_string):
    args = processing_args(args_string, 1, 1, 'use: birthday <name>')
    return contacts[args[0]].days_to_birthday()

@input_error
def parse_input(string):
    if re.search(r'[^A-Za-z0-9@\-\.\,\s\+]', string):
        raise ValueError('"'+string+'" not a valid command\nunsupported chars') 
    result = re.sub(r'[\s\,]+', ' ', string.strip())

    for command in FUNC_DICT:
        if result.lower().startswith(command):
            return (command, result[len(command):])

    raise ValueError(result.split()[0]+' not a valid command')


def add_default_records():
    records = ['add Ivan 0551112233 0320112299 0118885566',
    'add Ivan birthday 01-09-2001',
    'add Kate 0638885532 0935550112',
    'add Kate birthday 23-09-2004',
    'add Max 0321515822',
    'add Krysta 0912225566 0935556667 0995812244',
    'add Krysta birthday 09-03-1980']
    for record in records:
        command = parse_input(record)        
        FUNC_DICT[command[0]](command[1])

def main():
    add_default_records()
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

FUNC_DICT=  {'hello': hello, 'add': add, 'change': change, 'phone': phone,
            'show all': showall, 'exit': quit, 'good bye': quit, 'close': quit,
            'show': show, 'remove': remove, 'birthday': birthday}
contacts = AddressBook(dict())

if __name__ == '__main__':
    main()