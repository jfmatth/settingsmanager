import peewee, config, os 

db = peewee.SqliteDatabase(None)

class setting(peewee.Model):
    key = peewee.CharField()
    value = peewee.TextField()
    
    class Meta:
        database = db

def init(dbname='database.db'):
    # Initialize the DB connection, and make sure all the tables exist.
    db.init(os.path.join(config.module_path(), dbname) )
    
    if not setting.table_exists(): db.create_table(setting)