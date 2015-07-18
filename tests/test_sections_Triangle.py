import unittest
from operator import setslice
import sys

sys.path.insert(0, "..")
from sections.sections import Triangle
import test_sections_generic as generic



class ImplementationTests(unittest.TestCase):
    
    def setUp(self):
        self.triangle = Triangle()
        
    
    def test_ordering_of_vertices_does_not_change_area(self):
        # The Triangle class is based on Polygon which has negative area
        # if the vertices are ordered clockwise. Check that this behavior is
        # eliminated from Triangle.
        
        vertices = [(0, 0), (1, 0), (0, 1)]
        self.triangle[:] = vertices
        
        self.assertTrue(self.triangle.A > 0)        
        self.triangle[:] = vertices[-1::-1]
        self.assertTrue(self.triangle.A > 0, "Triangle area depends on ordering of vertices")
    
    
    def test_has_at_most_three_vertices(self):
        
        self.assertEqual(len(self.triangle), 0)
        
        self.triangle[:] = [(0, 0), (1, 0), (0, 1)]
        
        self.assertRaises(IndexError, self.triangle.append, (1, 1))
        self.assertRaises(IndexError, self.triangle.extend, [(1, 1)])
        self.assertRaises(IndexError, self.triangle.insert, 0, (1, 1))
        self.assertRaises(IndexError, setslice, self.triangle, 0, 3, [(0, 0), (1, 0), (0, 1), (1,1)])
        try:
            self.triangle[:] = [(0, 0), (1, 0)]
        except:
            self.fail("Failed to set triangle vertices by slicing")



class TestPhysicalProperties(generic.TestPhysicalProperties, unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.sectclass  = Triangle
        cls.vertices   = [(0, 0), (6, 10), (12, 2)]
        cls.dimensions = {}
        cls.rp         = 10.0, 5.0
        cls.A          = 54.0
        cls._I0        = 252.0, 324.0, 54.0
        cls._I         = 1116.0, 2268.0, 1350.0
        cls._cog       = 6.0, 4.0

    
    def get_section(self, density=1.0):
        triangle = self.sectclass(density=density)
        triangle[:] = self.vertices
        return triangle


    def scale_section_dimensions(self, factor, section=None):
    	if section is None:
    	    section = self.section
    	section[:] = [(factor*x1, factor*x2) for x1, x2 in self.vertices]
    
    
    def test_check_dimensions(self):
    	pass


if __name__ == "__main__":
    unittest.main()
