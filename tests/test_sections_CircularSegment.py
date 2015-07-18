import unittest
import sys
from math import pi

sys.path.insert(0, "..")
from sections.sections import CircularSegment
import test_sections_generic as generic


class TestPhysicalProperties(generic.TestPhysicalProperties, unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.sectclass  = CircularSegment
        cls.dimensions = dict(r=3.0, phi=pi/3)
        cls.rp         = 5.0, 4.0
        cls._cog       = 2.7598061133675302, 0.0
        cls.A          = 0.8152746633547157
        cls._I0        = 0.372950123661871, 0.009057844129888082, 0.0
        cls._I         = 0.372950123661871, 6.21862159920683, 0.0
    
    
    def scale_section_dimensions(self, factor, section=None):
    	if section is None:
    	    section = self.section
    	section.set_dimensions(r=factor*self.dimensions["r"])
    
    
    def test_check_dimensions(self):
    	self.assertRaises(ValueError, self.section.set_dimensions, r=-1)
    	self.assertRaises(ValueError, self.section.set_dimensions, r=0)
    	self.assertRaises(ValueError, self.section.set_dimensions, phi=-1)
    	self.assertRaises(ValueError, self.section.set_dimensions, phi=0)
    	self.assertRaises(ValueError, self.section.set_dimensions, phi=2.1*pi)
    

if __name__ == "__main__":
    unittest.main()
