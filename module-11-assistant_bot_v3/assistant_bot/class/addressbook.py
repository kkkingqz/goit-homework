from collections import UserDict
from record import *
from fields import *

class AddressBook(UserDict):

    def add_record(self, name, *values):
        if name not in self.data:
            self.data[name] = Record(name, values)
            return f'contact {name} created'

        return f'contact {name} already exists'

    def remove_record(self, name):
        self.data.pop(name)
        return f'contact {name} removed'
        
    def show(self, name, field_type=''):
        maxlen=80
        result = '*'*maxlen+'\n'
        result += ('|  {:^'+str(maxlen-6)+'}  |\n').format(self.data[name].name.upper())
        result += '*'*maxlen+'\n'
        
        if field_type:
            for count, value in enumerate(self.data[name].data[field_type]):
                result += ('|  {:^10}  |  {:^'+str(maxlen-21)+'}  |\n').format(f'{field_type} '+str(count+1), value)
                result += '-'*maxlen+'\n'
        else:
            for field_type in self.data[name].data:
                for count, value in enumerate(self.data[name].data[field_type]):
                    result += ('|  {:^10}  |  {:^'+str(maxlen-21)+'}  |\n').format(f'{field_type} '+str(count+1), value)
                    result += '-'*maxlen+'\n'

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