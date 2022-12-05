from logging import exception
from fields import *

class Record():
    def __init__(self, name, *phones) -> None:
        self.name = Name(name)
        self.phones = set()
        self.bithday = None
        if phones:
            for phone in phones:
                self.add_phone(phone)

    def add_phone(self, phone):
        self.phones.add(Phone(phone))
        return f'new phone for conact {self.name} added'
    
    def change_phone(self, oldphone, newphone):
        try:
            self.phones.remove(Phone(oldphone))
        except Exception as e:
            print(e)
            raise ValueError(f'phone {oldphone} not found')
        self.add_phone(newphone)
        return f'phone changed'

    def remove_phone(self, phone):
        try:
            self.phones.remove(Phone(phone))
        except Exception as e:
            raise ValueError(f'phone {phone} not found')
        return 'phone remove'

    def add_birthday(self, birthday):
        self.bithday = Birthday(birthday)

    def change_birhday(self, birthday):
        self.bithday = Birthday(birthday)

    def days_to_birthday(self):
        today = date.today()
        current_year_bd = self.birthday.birthday_current_year
        days = str((current_year_bd - today).days)
        return f'today is {today}. {self.name} birthday day in current year - {current_year_bd}\n{days} day(s)'
