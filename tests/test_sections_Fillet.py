import unittest
import sys
from math import pi

sys.path.insert(0, "..")
from sections.sections import Fillet
import test_sections_generic as generic


class TestPhysicalProperties(generic.TestPhysicalProperties, unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.sectclass  = Fillet
        cls.dimensions = dict(r=3.0, phi0=pi/3, phi1=pi*2/3)
        cls.rp         = 5.0, 4.0
        cls.A          = 6.16367930735052
        cls._I0        =  4.07970918156066, 5.09977122822122, 0.0
        cls._I         = 34.08506759985616, 5.09977122822122, 0.0
        cls._cog       = 0.0, 2.20637532613114
    
    
    def scale_section_dimensions(self, factor, section=None):
    	if section is None:
    	    section = self.section
    	section.set_dimensions(r=factor*self.dimensions["r"])
    	
    
    def test_check_dimensions(self):
    	self.assertRaises(ValueError, self.section.set_dimensions, r=-1)
    	self.assertRaises(ValueError, self.section.set_dimensions, r=0)
    	self.assertRaises(ValueError, self.section.set_dimensions, phi0=1, phi1=0)
    	self.assertRaises(ValueError, self.section.set_dimensions, phi0=1, phi1=1)
    	self.assertRaises(ValueError, self.section.set_dimensions, phi0=1, phi1=1 + 2.1*pi)


if __name__ == "__main__":
    unittest.main()
