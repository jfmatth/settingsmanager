import unittest

import settings

TESTDB = 'test.db'

class SimpleSettings_Basics(unittest.TestCase):
    '''
    Test the settings module.
    
    Store a pair of keys 
    '''
    k1 = "Key1"
    k2 = "Key2"
    
    v1 = 'Value 1'
    v2 = 'Value 2'
        
    c = None
        
    def setUp(self):
        self.c = settings.SettingsDict(dbname=TESTDB)
         
    def tearDown(self):
        del(self.c)

    def test_1Add(self):
        self.c[self.k1] = self.v1
        self.c[self.k2] = self.v2
        
    def test_2Recall(self):
        self.assertEqual(self.c[self.k1], self.v1)
        self.assertEqual(self.c[self.k2], self.v2)
        
    def test_3Overwrite(self):
        self.c[self.k1] = self.v1
        self.assertIn(self.k1, self.c)
        
    def test_4totalitems(self):
        self.assertTrue(len(self.c)==2)
        
class Settings_Identity(unittest.TestCase):
    def test_setIdentity(self):
        '''
        check that you can get and set the identity portion.
        '''
        s = settings.SettingsDict()
        
        x = s.get_identity()
        s.set_identity(x)
       
if __name__ == '__main__':
    unittest.main()

#     # lets fill up the dict from settings with interesting stuff
#     import os, stat
#     
#     c = settings.SettingsDict() 
#     
#     for root, dirs, files in os.walk("c:/cygwin/"):
#         for f in files:
#             fp = os.path.join(root,f)
#             
#             c[fp] = os.stat(fp)[stat.ST_SIZE]
#             print fp, c[fp]
