'''
dbmanager 

Holds all the peewee DB definitions

'''
import peewee, config, os 

DBNAME = "database.db"
DBPATH = config.module_path() 

db = peewee.SqliteDatabase(None)
class basetable(peewee.Model):
    '''
    defaults for all tables, only holds the DB attribute for now.
    '''
    class Meta:
        database = db

class setting(basetable):
    '''
    setting is the table for key / value pairs, used by the settings.py module.
    '''
    key = peewee.CharField(unique=True)     # unique creates a unique index.
    value = peewee.TextField()


    
def init(dbname=DBNAME, path=None):
    '''
    initialize the DB and all it's tables (if necessary)
    '''
    # Initialize the DB connection, and make sure all the tables exist.
    if path == None:
        path = DBPATH
        
    db.init(os.path.join(path, dbname) )
    
    if not setting.table_exists(): setting.create_table()
