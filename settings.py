'''
settings.py - Holds all settings for this setup (blah).
'''
import dbmanager

class SettingsDict(dict):
    '''
    a subclassed dict, which loads and saves it's values to a peewee database (sqllite) via the 
    dbmanager module.
    
    '''
    sTable = dbmanager.setting
    
    def __init__(self, *args, **kwargs):
        # we have to make sure our tables are there :)
        dbmanager.init()

        # load all the existing data from the settings table.
        for s in self.sTable.select():
            dict.__setitem__(self, s.key,s.value)
                
        dict.__init__(self, *args, **kwargs)
    
    def __setitem__(self, k, v):
        dict.__setitem__(self, k, v)
        self.sTable(key=k, value=v).save()