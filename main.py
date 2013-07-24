# main.py
'''
main.py - Starting program.
'''
import os
import logging
import logging.config

from settings import SettingsDict
import dbmanager
import logconfig       ## all our log settings are here for now.
logger = logging.getLogger("main")

# define a procedure that gets us out of this.
def stop():
    logger.debug("stop")

# initiate settings, settings don't actually need to be setup for this to run, just 
# nothing will happen :)
logger.debug("defining settings dict")
s = SettingsDict()

logger.debug("defining configinfo")
configinfo = {
              "settings" : s,
              "dbmodule" : dbmanager, 
              "stopfunc" : stop,  
              }

stop()