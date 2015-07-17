import unittest
from operator import concat, setitem, setslice

from sections.sections import Polygon, Rectangle
from tests.test_sections import SectionTests



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



class PolygonTests1(unittest.TestCase):

    def setUp(self):
        self.polygon = Polygon()
    

    def test_requires_at_least_three_vertices(self):

        self.assertRaises(ValueError, getattr, self.polygon, "A")
        self.assertRaises(ValueError, getattr, self.polygon, "_cog")
        self.assertRaises(ValueError, getattr, self.polygon, "_I0")
        
        self.polygon.append((0, 0))
        self.assertRaises(ValueError, getattr, self.polygon, "A")
        self.assertRaises(ValueError, getattr, self.polygon, "_cog")
        self.assertRaises(ValueError, getattr, self.polygon, "_I0")

        self.polygon.append((1, 0))
        self.assertRaises(ValueError, getattr, self.polygon, "A")
        self.assertRaises(ValueError, getattr, self.polygon, "_cog")
        self.assertRaises(ValueError, getattr, self.polygon, "_I0")

        self.polygon.append((0, 1))
        try:
            self.polygon.A
            self.polygon._cog
            self.polygon._I0
        except:
            self.fail("Not possible to calculate physical properties of polygon although it has three vertices")
    
    
    def test_cached_properties_are_reset_on_change_of_vertices(self):
        def error_raiser():
            raise ValueError
        self.polygon[:] = [(0, 0), (1, 0), (0, 1)]        
        self.polygon.reset_cached_properties = error_raiser
        
        self.assertRaises(ValueError, self.polygon.append, (1,1))
        self.assertRaises(ValueError, self.polygon.extend, [(1,1)])
        self.assertRaises(ValueError, self.polygon.insert, 0, (1,1))
        self.assertRaises(ValueError, setitem, self.polygon, 0, (1,1))
        self.assertRaises(ValueError, setslice, self.polygon, 0, 1, [(1,1)])


class PolygonTests2(unittest.TestCase, SectionTests):
    
    @classmethod
    def setUpClass(cls):
        cls.cls        = Polygon
        cls.dimensions = {}
        cls.vertices   = [(-1.0, -1.5), (1.0, -1.5), (1.0, 1.5), (-1.0, 1.5)]

        cls.rp         = 5.0, 4.0

        cls.rectangle  = Rectangle(a=2, b=3)
        cls.A          = cls.rectangle.A
        cls._I0        = cls.rectangle._I0
        cls._I         = cls._I0
        cls._cog       = cls.rectangle._cog
    
    
    def get_section(self, density=1.0):
        """
        A shortcut function to create a section with predefined dimensions."""
        polygon = self.cls(density=density)
        polygon[:] = self.vertices
        return polygon


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

