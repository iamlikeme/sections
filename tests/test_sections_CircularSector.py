import unittest
import sys
from math import pi

sys.path.insert(0, "..")
from sections.sections import CircularSector
import test_sections_generic as generic


class TestPhysicalProperties(generic.TestPhysicalProperties, unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.sectclass  = CircularSector
        cls.dimensions = {"ro":5.0, "ri":0.0, "phi":pi/3}
        cls.rp         = 3.0, 4.0
        cls.A          = 13.08996938995747
        cls._I         = 14.154074016574924, 149.47054335789346, 0.0
        cls._I0        = 14.154074016574924, 16.841424114647396, 0.0
        cls._cog       = 3.183098861837906, 0.0
    
    
    def scale_section_dimensions(self, factor, section=None):
    	if section is None:
    	    section = self.section
    	dimensions = dict(ro=factor*self.dimensions["ro"],
                          ri=factor*self.dimensions["ri"])
        section.set_dimensions(**dimensions)
    

    def test_check_dimensions(self):
    	self.assertRaises(ValueError, self.section.set_dimensions, ri=-1)
    	self.assertRaises(ValueError, self.section.set_dimensions, ro=-1)
    	self.assertRaises(ValueError, self.section.set_dimensions, ro= 0)
    	self.assertRaises(ValueError, self.section.set_dimensions, ro=1, ri=2)
    	self.assertRaises(ValueError, self.section.set_dimensions, phi=-0.1*pi)
    	self.assertRaises(ValueError, self.section.set_dimensions, phi=0)
    	self.assertRaises(ValueError, self.section.set_dimensions, phi=2.1 * pi)
    
    
    def test_todo(self):
        self.fail("TODO: Add tests for circular sector with ri>0")


if __name__ == "__main__":
    unittest.main()
