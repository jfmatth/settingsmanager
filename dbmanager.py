import peewee, config, os 


db = peewee.SqliteDatabase(None)
class basetable(peewee.Model):
    class Meta:
        database = db

class setting(basetable):
    key = peewee.CharField(unique=True, index=True)
    value = peewee.TextField()
    
    
class dicttable(basetable, dict):
    keyf = peewee.CharField(unique=True)
    dataf = peewee.CharField()

    
def init(dbname='database.db'):
    # Initialize the DB connection, and make sure all the tables exist.
    db.init(os.path.join(config.module_path(), dbname) )
    
    if not setting.table_exists(): db.create_table(setting)
    if not dicttable.table_exists(): db.create_table(dicttable)