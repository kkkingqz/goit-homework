import re
from input_error import *
from assistant_bot.class.addressbook import *

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
    args = processing_args(args_string, 3, 99, 'use:\n   add <name> <phone> [<phone2>, ...]')    
    return contacts.add_record(*args)

@input_error
def change(args_string):
    args = processing_args(args_string, 4, 4, 'use:\n   change <name> <field type> <old value> <new value>')    
    return contacts.change_record_field(*args)

@input_error
def phone(args_string):
    args = processing_args(args_string, 1, 1, 'use:\n   phone <name>')
    return contacts.show(args[0], field_type='phone')

@input_error
def show(args_string):
    args = processing_args(args_string, 1, 2, 'use:\n   show <name>\nor\n   show <name> <field type>')
    return contacts.show(*args)

@input_error
def showall(args_string):
    args = processing_args(args_string, 0, 0)
    return contacts.showall()

@input_error
def remove(args_string):
    args = processing_args(args_string, 1, 3, 'use:\n   remove <name>\n   or\n   remove <name> <field type>\n   or\n   remove <name> <field type> <value>')

    if len(args) == 1:
        return contacts.remove_record(args[0])

    if len(args) == 2:
        return contacts[args[0]].remove_field_type(args[1])

    if len(args) == 3:
        return contacts[args[0]].remove_field(args[1], args[2])

@input_error
def quit(args_string):
    args = processing_args(args_string, 0, 0)
    return 'Good bye!'

@input_error
def birthday(args_string):
    args = processing_args(args_string, 1, 1, 'use: birthday <name>')
    return contacts[args[0]].days_to_birthday()