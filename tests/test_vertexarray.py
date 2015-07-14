import unittest
from operator import setitem, getitem

from sections.core import VertexArray

class TestVertexArray(unittest.TestCase):

    def test_set_number_of_vertices(self):
        va1 = VertexArray()
        va2 = VertexArray(2)
        va3 = VertexArray()
        va3.n = 3
        
        self.assertEqual(len(va1), 0)
        self.assertEqual(len(va2), 2)
        self.assertEqual(len(va3), 3)


    def test_vertices_are_initially_None(self):
        va = VertexArray(1)
        self.assertRaises(ValueError, getitem, va, 0)
    

    def test_setting_vertices(self):
        va = VertexArray(1)
        
        self.assertRaises(TypeError, setitem, va, 0, 1.0)
        self.assertRaises(TypeError, setitem, va, 0, "ab")
        self.assertRaises(TypeError, setitem, va, 0, (None, None))
        self.assertRaises(TypeError, setitem, va, 0, (True, False))
        self.assertRaises(IndexError, setitem, va, 1, 1.0)
        
        # The following statements work
        va[0] = 1, 2
        va[0] = 1.0, 2.0
        va[0] = None
        
    
    def test_vertices_are_always_pairs_of_floats(self):
        va = VertexArray(2)
        va[0] = 1.0, 2.0
        va[1] = 1, 2
        
        self.assertTupleEqual(va[0], (1.0, 2.0))
        self.assertTupleEqual(va[1], (1.0, 2.0))
        

    def test_raise_value_error_on_getting_vertex_equal_to_None(self):
        va = VertexArray(1)
        va[0] = None
        
        self.assertRaises(ValueError, getitem, va, 0)

