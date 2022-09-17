import re
from collections import UserDict, UserString

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

class Record:
    def __init__(self, name, phone) -> None:
        self.name = Name(name)

        if isinstance(phone, str):
            self.phones = [Phone(phone)]
        elif isinstance(phone, list):
            self.phones = [Phone(p) for p in phone]

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        return f'add additional phone for contact: {self.name}'

    def change_phone(self, oldphone, newphone):
        try:
            index = self.phones.index(Phone(oldphone))
        except ValueError:
            raise ValueError('phone not found') 
        self.phones[index] = Phone(newphone)
        return 'phone change'

    def remove_phone(self, phone):
        try:
            index = self.phones.index(Phone(phone))
        except ValueError:
            raise ValueError('phone not found') 
        self.phones.pop(index)
        return 'phone removed'

class AddressBook(UserDict):
    def add_record(self, name, phone):
        try:
            self.data[name].add_phone(phone)
        except KeyError:
            self.data[name] = Record(name, phone)
            return f'contact {name} added'            

    def remove_record(self, name):
        if self.data.pop(name, None):
            return f'contact {name} removed'
        else:
            return f'contact {name} not found'

    def show(self, name, maxlen=80):
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

a1 = Record('Max', ['0636247300', '0501112233'])
#print(aa.phones)
contacts = AddressBook(dict())
contacts.add_record('Max', ['0636247300', '0501112233'])
contacts.add_record('Jack', ['0636247300'])
contacts.add_record('Jack', '5552233')
#print(contacts)
print(contacts.showall())
