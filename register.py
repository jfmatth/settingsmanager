'''
register.py 

The idea here is that we just have to get our 'identity' defaults, and then set them from our 
local information, sync that back to the server.

- if the server is off-line, it will fail, and we won't know if we are registered.
- if the server is on-line and we haven't synced before, it will create a record in the server system
  and bring down our various 'settings' for later.
- if the server is on-line and we've registered before, no harm no foul.

'''


import settings

import uuid
import socket
import sys

def main(remoteID=None):

    s = settings.SettingsDict()
    
    # set the server IP
    if not remoteID== None:
        s.set_remote(remoteID)

    # save our identity    
    ident = s.get_identity()
    print "identity currently"
    print s
    
    ident['ipaddr']   = socket.gethostbyname_ex(socket.gethostname() )[2][0]
    ident['hostname'] = socket.gethostbyname_ex(socket.gethostname() )[0]
    ident['macaddr']  = hex(uuid.getnode())
    s.set_identity(ident)
    print s
    
    s.update_remote(fail_silently=False)
    
    print "Registered"
    print s
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print "Not registered"
