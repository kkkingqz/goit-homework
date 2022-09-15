import re
from collections import defaultdict#, namedtuple

def hello(args):
    return 'How can I help you?'

def add(args):
    if len(args) != 2:
        raise Exception('too many args')
    elif not (isname(args[0]) and isphone(args[1])):
        raise Exception('incorrect args')
    else:
        update_record(args[0], args[1])

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

def input_error(func):
    def inner(string):
        try:
            func(string)
        except Exception as err:
            print(err)
    return inner

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
    for command in func_dict.keys():
        if result.startswith(command):
            return func_dict[command](result.lstrip(command).split())
    raise Exception(result.split()[0]+' not a valid command')
    #if len(result) > 4



def update_record(name, phone):
    users_dict[name] = phone

func_dict={'hello': hello, 'add': add, 'change': change, 'phone': phone, 'show all': showall, 'quit': quit}
users_dict=dict()
#Record = namedtuple('Record', ['name', 'phone'])


while True:
    a=input('>>> ')
    check_input(a)
    parse_input(a)
    
