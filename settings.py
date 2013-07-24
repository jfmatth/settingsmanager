import xmlrpclib
import logging

import dbmanager

logger = logging.getLogger(__name__)

IDVERSION = 1.00

class SyncWebException(Exception):
    pass 

class SettingsDict(dict):
    '''
    A dict class that saves it's values to a local DB and allows a read-only sync from a remote RPC
    server.

    uses the dbmanager (peewee) library to sync with a database.  dbmanager is the main DB interface
    for all DB related functions in this environment.
    '''
    RPCPATH    = "/rpc/"           # URL path to the RPCXML functions.
    RPCSERVER  = 'rpcserver'       # key value required for syncweb to work, address of our server.

    sTable = dbmanager.setting     # the DB table holding our values.

    def __init__(self, *args, **kwargs):
        '''
        setup link to local DB, load it's items with the DB's cache, call init.
        '''
        # we have to make sure our tables are there :)
        if "dbname" in kwargs:
            dbmanager.init(dbname=kwargs['dbname'])
            kwargs.pop('dbname')            # take off the keyword, otherwise it ends up in the dictionary.
        else:
            dbmanager.init()

        # load all the existing data from the settings table.
        for s in self.sTable.select():
            dict.__setitem__(self, s.key,s.value)

        # if we can, we should sync with the web server.
        self.sync_remote()

        dict.__init__(self, *args, **kwargs)
        
    def __setitem__(self, k, v):
        '''
        provide logic to see if the DB needs a replace or new item (built into dict already)
        '''
        if self.has_key(k):
            # get the object from the DB, and update it.
            r = self.sTable.get(key=k)
            r.value = v 
        else:
            r = self.sTable(key=k, value=v) 

        r.save()

        dict.__setitem__(self, k, v)

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).iteritems():
            self[k] = v

    def set_remote(self, serverIP):
        if not serverIP == None:
            self[self.RPCSERVER] = serverIP

    def sync_remote(self, fail_silently = True):
        '''
        Sync all our settings with the main RPC server.
        Requires that there are certain settings in the DB / dict to find the server.
        
        fail_silently - requires that the value for RPCSERVER key be present in the dictionary to test with.
        '''
        logger.debug("sync_remote")
        if self.has_key(self.RPCSERVER):
            # try to sync with the main web server.
            # create the full URL for our RPC server
            logger.debug("connecting to RPC server %s%s" % (self[self.RPCSERVER],self.RPCPATH) )
            svrpath = self[self.RPCSERVER] + self.RPCPATH
            rpc = xmlrpclib.ServerProxy(svrpath, allow_none=True)

            # we ignore any RPC errors unless we don't want to
            try:
                self.update( rpc.settings(self.get_identity()) )
                logger.info("Synchronized")
            except:
                logger.warning("sync failed")
                if fail_silently:
                    logger.info("Offline")
                else:
                    logger.critical("Sync failed, raising exception")
                    raise
        else:
            if not fail_silently:
                raise SyncWebException("%s key not defined in SettingsDict" % self.RPCSERVER)
            else:
                return "No %s key defined" % self.RPCSERVER

    def get_identity(self):
        '''
        Returns a dictionary with the parameters that define this system.
        '''
        logger.debug("get_identity")
        
        idparams = {}
        idparams['guid']      = self.get('guid')
        idparams['ipaddr']    = self.get('ipaddr')
        idparams['hostname']  = self.get('hostname')
        idparams['macaddr']   = self.get('macaddr')
        idparams['idversion'] = IDVERSION 
        
        return idparams

    def set_identity(self, idparams):
        '''
        Pretty much the opposite of get_identity, but this provides a method to set the personality of this
        system.
        
        Example of usage for first time:
        
        x = settings.get_identity()  # this will be a blank dictionary with only the version set.
        x['guid']     = <some value for uniquely identifying a system>
        x['ipaddr']   = socket.gethostbyname_ex(socket.gethostname() )[2][0]
        x['hostname'] = socket.gethostbyname_ex(socket.gethostname() )[0]
        x['macaddr']  = uuid.getnode()
        settings.set_identity(x)
        '''
        logger.debug("set_identity")
        
        if type(idparams) == dict:
            for k,v in idparams.iteritems():
                if not v==None:                 # we don't save None's 
                    self[k] = v