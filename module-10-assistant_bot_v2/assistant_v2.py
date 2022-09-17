import re
from collections import UserDict, UserString

class Field(UserString):
    def __init__(self, seq: object) -> None:
        super().__init__(seq)
        self.value = self.data #создаем value следуя букве ТЗ. так то тут это не нужно

class Phone(Field):
    pass

class Name(Field):
    pass

class Record:
    def __init__(self, name, phone) -> None:
        self.name = Name(name)
        self.phones = [Phone(phone)]

    def __repr__(self) -> str:
        pass#выводим список всех телефонов

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
