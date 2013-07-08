'''
settings.py - Holds all settings for this setup (blah).
'''
import dbmanager



class SyncWebException(Exception):
    pass 

class SettingsDict(dict):
    '''
    a subclassed dict, which loads and saves it's values to a peewee database (sqllite) via the 
    dbmanager module.
    
    '''
    RPCPATH       = "/rpc/"           # URL path to the RPCXML functions.
    RPCSERVERKEY  = 'rpcserver'       # key value required for syncweb to work, address of our server.
    
    sTable = dbmanager.setting

    def __init__(self, *args, **kwargs):
        # we have to make sure our tables are there :)
        if "dbname" in kwargs:
            dbmanager.init(dbname=kwargs['dbname'])
            kwargs.pop('dbname')            # take off the keyword, otherwise it ends up in the dictionary.
        else:
            dbmanager.init()

        # load all the existing data from the settings table.
        for s in self.sTable.select():
            dict.__setitem__(self, s.key,s.value)

        dict.__init__(self, *args, **kwargs)
        
        # see if we can sync our settings with the web.
        self.syncweb()

    def __setitem__(self, k, v):
        if self.has_key(k):
            r = self.sTable.get(key=k) 
            # get the object from the DB, and update it.
        else:
            r = self.sTable(key=k, value=v) 

        r.save()

        dict.__setitem__(self, k, v)

    def syncweb(self, fail_silently = True):
        '''
        Sync all our settings with the main RPC server.
        Requires that there are certain settings in the DB / dict to find the server.
        '''
        if self.has_key(self.RPCSERVERKEY):
            # try to sync with the main web server.
            pass
        else:
            if not fail_silently:
                raise SyncWebException("%s not defined in SettingsDict" % self.RPCSERVERKEY)
