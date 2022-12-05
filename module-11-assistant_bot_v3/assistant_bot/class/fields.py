import re
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
        return self.__value
    @value.setter
    def value(self, value):
        if not re.search(r'[^0-9]', self.sanitize_phone_number(value)):
            self.__value = self.sanitize_phone_number(value)
        else:
            raise ValueError('incorrect phone number')

class Name(Field):
    pass

class EMail(Field):
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
            self.__value = Dateparse.parse(string).date() #see line 6
        except Dateparse._parser.ParserError:
            raise ValueError('incorrect date format. enter yyyy-mm-dd')
