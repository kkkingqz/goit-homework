import re

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

    update_record(args[0], sanitize_phone_number(args[1]))
    return f'user {args[0]} added'

@input_error
def change(args_string):
    args = args_string.split()

    if len(args) != 2:
        raise ValueError('incorrect args\nplease enter: change <name> <phone>')

    if not (isname(args[0]) and isphone(args[1])):
        raise ValueError('incorrect name or phone')

    update_record(args[0], sanitize_phone_number(args[1]))
    return f'user {args[0]} changed'

@input_error
def phone(args_string):
    if len(args_string.split()) != 1:
        raise ValueError('please enter a name')

    name = args_string.strip()

    if not isname(name):
        raise ValueError('incorrect name')

    return get_record(name)

@input_error
def showall(args_string):
    if args_string:
        raise ValueError('incorrect args\nuse "show all" without args')
    str = ''
    for name, phone in USERS_DICT.items():
        str += f'{name}: {phone}\n'
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
    
def update_record(name, phone):
    USERS_DICT[name] = phone

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

if __name__ == '__main__':
    main()