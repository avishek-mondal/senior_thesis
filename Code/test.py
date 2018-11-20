import sys

a = {'a':'dog', 'b': 'lol'}
b={}
b = dict.fromkeys(list(a.keys()),'')

print(b)
