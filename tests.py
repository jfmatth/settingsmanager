import unittest, os

import settings

class SimpleSettingsTest(unittest.TestCase):
    '''
    Test the settings module.
    
    Store a pair of keys 
    '''
    k1 = "Key1"
    k2 = "Key2"
    
    v1 = 'Value 1'
    v2 = 'Value 2'
        
    def setUp(self):
        self.c = settings.SettingsDict()
        
    def tearDown(self):
        del(self.c)
        
    def test_1Add(self):
        self.c[self.k1] = self.v1
        self.assertIn(self.k1, self.c)
        
        self.c[self.k2] = self.v2
        self.assertIn(self.k2, self.c)
        
    def test_2Recall(self):
        self.assertEqual(self.c[self.k1], self.v1)
        self.assertEqual(self.c[self.k2], self.v2)
        
    def test_3Overwrite(self):
        self.c[self.k1] = self.v1
        self.assertIn(self.k1, self.c)

if __name__ == '__main__':
    unittest.main()
