import unittest
import htmlp

class TestHp(unittest.TestCase):
    def setUp(self):
        self.hp = htmlp.Hp()

    def test_parsePage1(self):
        self.hp.parsePage('http://www.misawa.co.jp/')
        self.assertTrue( len(self.hp.links) > 0)

    def test_parsePage2(self):
        self.hp.parsePage('http://www.jins.com/')
        self.assertTrue( len(self.hp.links) > 0)

if __name__ == '__main__':
    unittest.main()


