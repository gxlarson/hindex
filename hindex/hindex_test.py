import unittest
import hindex


class TestHIndex(unittest.TestCase):

    def test_empty_list(self):
        l = []
        h = hindex.h_index(l)
        self.assertEqual(h, 0)
    
    def test_sequence(self):
        l = [1,2,3,4,5,6,7,8,9,10]
        h = hindex.h_index(l)
        self.assertEqual(h, 5)
    
    def test_all_ones(self):
        l = [1,1,1,1,1,1,1,1,1]
        h = hindex.h_index(l)
        self.assertEqual(h, 1)

    def test_all_zeros(self):
        l = [0,0,0,0,0,0,0,0,0]
        h = hindex.h_index(l)
        self.assertEqual(h, 0)
    
    def test_one(self):
        l = [1]
        h = hindex.h_index(l)
        self.assertEqual(h, 1)

    def test_five(self):
        l = [5]
        h = hindex.h_index(l)
        self.assertEqual(h, 1)
    
    def test_all_five(self):
        l = [5,5,5,5,5,5,5,5,5,5]
        h = hindex.h_index(l)
        self.assertEqual(h, 5)
        l = [5,5,5]
        h = hindex.h_index(l)
        self.assertEqual(h, 3)
    
    def test_several(self):
        l = [1000000, 3, 2, 1]
        h = hindex.h_index(l)
        self.assertEqual(h, 2)
        l = [900, 2, 10, 4, 1]
        h = hindex.h_index(l)
        self.assertEqual(h, 3)
        l = [150, 30, 20, 10, 9, 8, 3, 1, 0, 0]
        h = hindex.h_index(l)
        self.assertEqual(h, 6)


class TestI10Index(unittest.TestCase):

    def test_simple(self):
        l = [10, 20, 30, 19, 8, 9, 0, 33, 10101]
        i10 = hindex.i10_index(l)
        self.assertEqual(i10, 6)
        l = [11]
        i10 = hindex.i10_index(l)
        self.assertEqual(i10, 1)
        l = [1,2,3,4,5,6,7,8,9]
        i10 = hindex.i10_index(l)
        self.assertEqual(i10, 0)
    
    def test_empty(self):
        l = []
        i10 = hindex.i10_index(l)
        self.assertEqual(i10, 0)


if __name__ == '__main__':
    unittest.main()