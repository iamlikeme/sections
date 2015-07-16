import unittest

from sections.sections import Rectangle
from tests.test_section import SectionTests

class RectangleTests(unittest.TestCase, SectionTests):
    
    def setUp(self):
        self.a          = 2.0
        self.b          = 3.0
        self.cls        = Rectangle
        self.dimensions = {"a":self.a, "b":self.b}
        self.rp         = 5.0, 4.0
        self.A          = 6.0
        self._I0        = 4.5, 2.0, 0.0
        self._I         = self._I0
        self._cog       = 0.0, 0.0
        
    
    def test_check_dimensions(self):
    	rect = Rectangle(a=1, b=2)
    	self.assertRaises(ValueError, rect.set_dimensions, a=-1)
    	self.assertRaises(ValueError, rect.set_dimensions, b=-1)
    	self.assertRaises(ValueError, rect.set_dimensions, a=0)
    	self.assertRaises(ValueError, rect.set_dimensions, b=0)
