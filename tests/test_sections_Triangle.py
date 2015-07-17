import unittest
from operator import setslice

from sections.sections import Triangle
from tests.test_sections import SectionTests


class TriangleTests(unittest.TestCase):
    
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



class TrianglePhysicalProperties(unittest.TestCase, SectionTests):
    
    @classmethod
    def setUpClass(cls):
        cls.cls        = Triangle
        cls.vertices   = [(0, 0), (6, 10), (12, 2)]
        cls.dimensions = {}
        cls.rp         = 10.0, 5.0
        cls.A          = 54.0
        cls._I0        = 252.0, 324.0, 54.0
        cls._I         = 1116.0, 2268.0, 1350.0
        cls._cog       = 6.0, 4.0

    
    def get_section(self, density=1.0):
        triangle = self.cls(density=density)
        triangle[:] = self.vertices
        return triangle


    def test_dimensions(self):
        sec = self.get_section()
        # Evaluate properties
        sec.A
        sec._I0
        sec._I
        
        # Check if properties change when dimensions are changed
        scale = 2.0
        sec[:] = [(scale*x1, scale*x2) for x1, x2 in self.vertices]
        self.assertEqual(sec.A, scale**2 * self.A)
        self.assertEqual(sec._I0, tuple(scale**4*i for i in self._I0))
        self.assertEqual(sec._I, tuple(scale**4*i for i in self._I))

