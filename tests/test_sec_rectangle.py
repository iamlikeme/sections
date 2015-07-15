import unittest

from sections.sections import Rectangle
from sections.core import SimpleSection


class RectangleTests(unittest.TestCase):

    def test_class(self):
        rec = Rectangle(a=2.0, b=3.0)

        self.assertIsInstance(rec, SimpleSection)        
        self.assertTrue(hasattr(rec, "a"))
        self.assertTrue(hasattr(rec, "b"))
    
    
    def test_area(self):
        a, b = 2.0, 3.0
        rec  = Rectangle(a=a, b=b)
        
        self.assertEqual(rec.A, a*b)
    
    
    def test_density(self):
        a, b = 2.0, 3.0
        rec  = Rectangle(a=a, b=b, density=2)
        
        self.assertEqual(rec.A, 2*a*b)
        
        rec.set_density(-3)
        self.assertEqual(rec.A, -3*a*b)
    
    
    def test_position(self):
        a, b = 2.0, 3.0
        rec  = Rectangle(a=a, b=b)
        
        rec.set_position(1, 2, 3)
        self.assertEqual(rec.A, a*b)
    
    
    def test_dimensions(self):
        a, b = 2.0, 3.0
        rec  = Rectangle(a=a, b=b)

        A = rec.A
        rec.set_dimensions(a=2*a, b=2*b)
        self.assertEqual(rec.A, 4*A)
        
