import unittest
from operator import concat, setitem

from sections.sections import Polygon



class SubclassingFromList(unittest.TestCase):
    
    def setUp(self):
        self.polygon = Polygon()
    
    
    def test_append(self):
        self.assertTrue(len(self.polygon)==0)
        self.assertRaises(TypeError, self.polygon.append, 1)
        self.assertRaises(ValueError, self.polygon.append, (1, 2, 3))
        
        self.polygon.append((1, 2))
        self.assertTrue(len(self.polygon)==1)
        self.assertTupleEqual(self.polygon[0], (1.0, 2.0))
        self.assertTrue(all(isinstance(x, float) for x in reduce(concat, self.polygon)) )
        
    
    def test_extend(self):

        self.assertTrue(len(self.polygon)==0)
        self.assertRaises(TypeError, self.polygon.extend, (1, 2))
        self.assertRaises(ValueError, self.polygon.extend, [(1,2,3), (4,5,6)])
        
        self.polygon.extend([(1, 2), (3, 4)])
        self.assertTrue(len(self.polygon)==2)
        self.assertTupleEqual(self.polygon[0], (1.0, 2.0))
        self.assertTupleEqual(self.polygon[1], (3.0, 4.0))
        self.assertTrue(all(isinstance(x, float) for x in reduce(concat, self.polygon)) )
        
    
    def test_setitem(self):
        
        self.polygon.append((0,0))
        self.polygon[0] = (1, 2)
        
        self.assertRaises(IndexError, setitem, self.polygon, 1, (1,2))
        self.assertTupleEqual(self.polygon[0], (1.0, 2.0))
        self.assertTrue(all(isinstance(x, float) for x in reduce(concat, self.polygon)) )
    
    
    def test_setslice(self):
        
        self.polygon[:] = [(1, 2), (3, 4)]

        self.assertTrue(len(self.polygon)==2)
        self.assertTupleEqual(self.polygon[0], (1.0, 2.0))
        self.assertTupleEqual(self.polygon[1], (3.0, 4.0))
        self.assertTrue(all(isinstance(x, float) for x in reduce(concat, self.polygon)) )
    
    
    def test_insert(self):
        
        self.polygon[:] = [(1, 2), (3, 4)]
        self.polygon.insert(1, (5, 6))

        self.assertTrue(len(self.polygon)==3)
        self.assertTupleEqual(self.polygon[1], (5.0, 6.0))
        self.assertTrue(all(isinstance(x, float) for x in reduce(concat, self.polygon)) )

