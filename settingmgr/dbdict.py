from db import Setting, dbInit
import json
import logging
import requests
import socket
from uuid import getnode as get_mac

logger = logging.getLogger(__name__)

class DBDict(dict):
    def __init__(self, name="dbdict.db"):
            
        logger.debug("Calling dbinit")
        dbInit(name)
        
        logger.debug("Updating all my items from the DB")
        for s in Setting.select():
            dict.__setitem__(self, s.key,s.value)

        dict.__init__(self)

    def __setitem__(self, k, v):
        '''
        provide logic to see if the DB needs a replace or new item (built into dict already)
        '''
        logger.debug("_setitem_")
        if self.has_key(k):
            # get the object from the DB, and update it.
            r = Setting.get(key=k)
            r.value = v 
        else:
            r = Setting(key=k, value=v) 

        logger.debug("Saving item to DB")
        r.save()

        dict.__setitem__(self, k, v)

    def __delitem__(self, k):
        logger.debug("__delitem__")
        r = Setting.get(key=k)
        r.delete_instance()

        return dict.__delitem__(self, k)


    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).iteritems():
            self[k] = v


# class RemoteDict(DBDict):
#     # this is mainly a behavior class for subclasses that want to override the behavior methods.
# 
#     def __init__(self, *args, **kwargs):
#         super(RemoteDict, self).__init__(*args, **kwargs)
#         
#         # once we are initialized, we call Sync to get the latest data up and down.
#         self.Sync()
# 
#     def _remoteid(self):
#         # whatever our remote id is (url, xmlrpc setup, etc
#         return None
# 
#     def _remoteSyncUp(self, data):
#         pass
#     
#     def _remoteSyncDown(self):
#         pass
#     
#     def Sync(self):
#         logger.debug("Sync")
#         if self._remoteid():
# 
#             # send it up to the remote system
#             logger.debug("Calling _remoteSyncup")
#             self._remoteSyncUp()
# 
#             #pull down anything we need
#             logger.debug("Calling _remoteSyncDown") 
#             self._remoteSyncDown()
            

class RemoteUrlDict(DBDict):
    # This class will sync to the "remoteid" server via json.

    def __init__(self, *args, **kwargs):
        super(RemoteUrlDict, self).__init__(*args, **kwargs)
         
        # once we are initialized, we call Sync to get the latest data up and down.
        self.Sync()

    
    def _showsyncerror(self):
        # do we display an error when the remote sync fails.
        return self.get("showsyncerror", True)

    def _remoteURL(self):
        return None
    
    def _SettingPath(self):
        ## this is appended to the self._remoteURL
        return None
    
    def _RegisterPath(self):
        ## this is appended to the self._remoteURL
        return None
    
    def _remoteid(self):
        return None

    def _remoteSyncUp(self):
        # push the data to the remote
        url = "%s%s" % (self._remoteURL(), self._SettingPath() )
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, data=json.dumps(self), headers=headers)
        print("%s" % r.status_code)
    
    def _remoteSyncDown(self):
        # pull it all down from the server
        url = "%s%s" % (self._remoteURL(), self._SettingPath() )
        r = requests.get(url)
        if r.json():
            self.update(r.json() )

    def Sync(self):
        logger.debug("Sync")
        try:
            if self._remoteURL() and self._SettingPath():
                # send it up to the remote system
                logger.debug("Calling _remoteSyncup")
                self._remoteSyncUp()
    
                #pull down anything we need
                logger.debug("Calling _remoteSyncDown") 
                self._remoteSyncDown()
        except:
            logger.error("Error on Sync()")
            print "Error on sync()"


class SettingDict(RemoteUrlDict):

    def _remoteURL(self):
        return self.get('remoteurl', None)

    def _remoteid(self):
        return self.get("uniqueid", None)

    def _SettingPath(self):
        return "/setting/%s/" % self._remoteid()

    def _RegisterPath(self):
        return "/register/"

    def register(self):
        if self._remoteURL() and self._RegisterPath():
            url = "%s%s" % (self._remoteURL(), self._RegisterPath() )
            headers = {'Content-Type': 'application/json'}

            sockinfo = socket.gethostbyname_ex(socket.gethostname() )
            regparams = {'macaddr':hex(get_mac()),
                         'ipaddr': sockinfo[2][0] ,
                         'hostname':sockinfo[0]
                        }
            r = requests.post(url, data = json.dumps(regparams), headers=headers)
            if r.status_code == 200 and r.json():
                self.update(r.json() )
            
        else:
            print "No remote information"
            
    def _remoteSyncUp(self):
        pass
        