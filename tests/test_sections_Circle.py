import unittest

from sections.sections import Circle
from tests.test_sections import SectionTests

class CircleTests(unittest.TestCase, SectionTests):
    
    def setUp(self):
        self.r          = 3.0
        self.cls        = Circle
        self.dimensions = {"r":self.r}
        self.rp         = 5.0, 4.0
        self.A          = 28.274333882308138
        self._I0        = 63.61725123519331, 63.61725123519331, 0.0
        self._I         = self._I0
        self._cog       = 0.0, 0.0
    
    
    def test_check_dimensions(self):
    	circle = Circle(r=1)
    	
    	self.assertRaises(ValueError, circle.set_dimensions, r=-1)
    	self.assertRaises(ValueError, circle.set_dimensions, r=0)
