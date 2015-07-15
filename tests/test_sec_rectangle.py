import unittest

from sections.sections import Rectangle
from sections.core import SimpleSection


class RectangleTests(unittest.TestCase):
    
    def setUp(self):
        self.a    = 2.0
        self.b    = 3.0
        self._cog = 0.0, 0.0
        self.A    = self.a * self.b
        self._I0  = self.a * self.b**3 / 12., \
                    self.b * self.a**3 / 12., \
                    0.0
        self._I    = self._I0

    
    def test_properties_in_local_csys(self):
        rec  = Rectangle(a=self.a, b=self.b)
        
        self.assertEqual(rec.A, self.A)
        self.assertEqual(rec._cog, self._cog)
        self.assertEqual(rec._I0, self._I0)
        self.assertEqual(rec._I, self._I)
        
    
    def test_density(self):
        rec  = Rectangle(a=self.a, b=self.b, density=2)

        self.assertEqual(rec._cog, self._cog)
        self.assertEqual(rec.A, 2*self.A)
        self.assertEqual(rec._I0, tuple(2*i for i in self._I0))
        self.assertEqual(rec._I, tuple(2*i for i in self._I))
        
        rec.set_density(-3)
        self.assertEqual(rec._cog, self._cog)
        self.assertEqual(rec.A, -3*self.A)
        self.assertEqual(rec._I0, tuple(-3*i for i in self._I0))
        self.assertEqual(rec._I, tuple(-3*i for i in self._I))
    
    
    def test_position(self):
        rec  = Rectangle(a=self.a, b=self.b)
        
        rec.set_position(1, 2, 3)
        self.assertEqual(rec.A, self.A)
    
    
    def test_dimensions(self):
        rec  = Rectangle(a=self.a, b=self.b)

        rec.set_dimensions(a=2*self.a, b=2*self.b)
        self.assertEqual(rec.A, 4*self.A)
        
