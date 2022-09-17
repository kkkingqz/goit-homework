from collections import defaultdict
from re import A

t = defaultdict(list)

t['a'].append(1)

b = t['a']

print(b)
t['a'].append(2)
print(t['a'])
print(b)
