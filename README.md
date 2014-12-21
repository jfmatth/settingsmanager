### Setting Dictionary (seetingdict)

A subclass of dict that saves things in a local sqlite DB.  

Requirements : peewee ORM 2.4.*

Sample usage
```
from settingsdict import SettingsDict
s = SettingsDict()

s['a'] = 1234
s['b'] = 2345

print s
{u'a': u'1234', u'b': u'2345'} 

del(s)
s = SettingsDict()
print s
{u'a': u'1234', u'b': u'2345'} 
```

SettingDict takes an optional name argument.  Name is the name of the database you want to create.
