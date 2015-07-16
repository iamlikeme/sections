import unittest
from operator import setitem, getitem, setslice, getslice

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
    
    
    def test_resizing(self):
        va1 = VertexArray()
        va1.n = 1
        
        va2 = VertexArray(1)
        va2[0] = 1.0, 2.0
        va2.n  = 2
        
        va3 = VertexArray(2)
        va3[0] = 1.0, 2.0
        va3[1] = 3.0, 4.0
        va3.n  = 1
        
        self.assertEqual(len(va1), 1)
        self.assertRaises(ValueError, getitem, va1, 0)  # The added vertex should be unset
        
        self.assertEqual(len(va2), 2)
        self.assertTupleEqual(va2[0], (1.0, 2.0))
        self.assertRaises(ValueError, getitem, va2, 1)
        
        self.assertEqual(len(va3), 1)
        self.assertTupleEqual(va3[0], (1.0, 2.0))

        
    def test_getslice(self):
        vertices = [(1.0, 2.0), (3.0, 4.0), (5.0, 6.0)]
        va = VertexArray(3)
        va[:] = vertices
        
        self.assertListEqual(va[1:], vertices[1:])
        self.assertListEqual(va[:-1], vertices[:-1])
        self.assertListEqual(va[-1::], vertices[-1::])
    
    
    def test_setslice(self):
        # Using two lists of vertices - one with ints and one with floats
        # This is to check that all numbers are converted to floats when setting a slice
        _vertices = [(1, 2), (3, 4)]
        vertices  = [(1.0, 2.0), (3.0, 4.0)]
        va1 = VertexArray(1)
        va2 = VertexArray(2)
        va2[:] = _vertices
        
        # Do not allow to change array length
        self.assertRaises(ValueError, setslice, va1, 0, 1, vertices)
        self.assertRaises(ValueError, setslice, va2, 0, 2, vertices[:1])

        self.assertEqual(va2[0], vertices[0])
        self.assertEqual(va2[1], vertices[1])
        self.assertIsInstance(va2[0][0], float)


    def test_copy(self):
        va1 = VertexArray(2)
        va1[:] = (1,2), (3,4)
        va2 = va1.copy()
        
        self.assertIsInstance(va2, va1.__class__)
        self.assertListEqual(va1[:], va2[:])

