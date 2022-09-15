import re
from collections import defaultdict#, namedtuple

def input_error(func):
    def inner(string):
        try:
            ret = func(string)
            return ret
        except Exception as err:
            return err
    return inner

@input_error
def hello(args_string):
    if args_string:
        raise Exception('incorrect args')
    return 'How can I help you?'

@input_error
def add(args_string):
    args = args_string.split()
    if len(args) != 2:
        raise Exception('incorrect args')
    elif not (isname(args[0]) and isphone(args[1])):
        raise Exception('incorrect args')
    else:
        update_record(args[0], args[1])
        return 'user '+args[0]+' added'

def change(args):
    pass

def phone(args):
    pass

def showall(args):
    pass

def quit(print):
    if not print:
        exit()
    else:
        return 'Good bye!'

def check_input(string):
    return bool(not re.search(r'[^A-Za-z0-9\.\,\s\+]', string))

def isname(string):
    return bool(not re.search(r'[^A-Za-z]', string))

def sanitize_phone_number(phone):
    return phone.replace(' ','').replace('(','').replace(')','').replace('+','').replace('-','')

def isphone(string):
    return bool(not re.search(r'[^0-9]', sanitize_phone_number(string)))

@input_error
def parse_input(string):
    if not check_input(string):
        raise Exception('"'+string+'" not a valid command\nunsupported chars') 
    result = re.sub(r'[\s\,]+', ' ', string.strip().lower())
    
    for command in FUNC_DICT:
        if result.lower().startswith(command):
            return (command, result[len(command):])#.lstrip(command)#func_dict[command](result.lstrip(command))
    raise Exception(result.split()[0]+' not a valid command')
    



def update_record(name, phone):
    USERS_DICT[name] = phone

FUNC_DICT={'hello': hello, 'add': add, 'change': change, 'phone': phone, 'show all': showall, 'quit': quit}
USERS_DICT=dict()
#Record = namedtuple('Record', ['name', 'phone'])


while True:
    #a=input('>>> ')
    #check_input(a)
    command = parse_input(input('>>> '))
    if isinstance(command, str) or isinstance(command, Exception):
        print(command)
    elif isinstance(command, tuple):
        print(FUNC_DICT[command[0]](command[1]))
    else:
        print('something was wrong')
    #print (users_dict)
