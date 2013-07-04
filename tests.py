import unittest, os

import settings

class SimpleSettingsTest(unittest.TestCase):
    str1 = 'this is a test'
    str2 = 'this is the second test in the dictionary'
        
    def setUp(self):
        self.c = settings.SettingsDict()
        
    def tearDown(self):
        del(self.c)
        
    def testAdd(self):
        self.c['str1'] = self.str1
        self.c['str2'] = self.str2
        
    def testRecall(self):
        self.assertEqual(self.c['str1'], self.str1)
        self.assertEqual(self.c['str2'], self.str2)

if __name__ == '__main__':
    unittest.main()
