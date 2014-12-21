import peewee
import argparse

db = peewee.SqliteDatabase("settings.db")

class basetable(peewee.Model):
    '''
    defaults for all tables, only holds the DB attribute for now.
    '''
    class Meta:
        database = db

class Setting(basetable):
    '''
    setting is the table for key / value pairs, used by the settingsdict.py module.
    '''
    key = peewee.CharField(unique=True)     # unique creates a unique index.
    value = peewee.TextField(null=True)

    def All(self):
        return self.select()

def Init():
        print("Initializing Database") 
        db.connect()
        db.create_tables([Setting], safe=True)
        
if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-I", "--init", help="Initialize the database", action="store_true")
    args = parser.parse_args()

    if args.init:   
        Init()

