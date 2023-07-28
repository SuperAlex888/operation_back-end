import unittest

class TestExample(unittest.TestCase):
    def test_lists_equal(self):
        list1 = [1, 2, 3]
        list2 = [1, 2]
        self.assertListEqual(list1, list2)

if __name__ == '__main__':
    unittest.main()
