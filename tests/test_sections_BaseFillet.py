import unittest
import sys
from math import pi

sys.path.insert(0, "..")
from sections.sections import BaseFillet
import test_sections_generic as generic


class TestPhysicalProperties1(generic.TestPhysicalProperties, unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.sectclass  = BaseFillet
        cls.dimensions = dict(r=3.0, phi=pi/3)
        cls.angular    = ["phi"]
        cls.rp         = 5.0, 4.0
        cls.A          = 6.16367930735052
        cls._I0        = 5.09977122822122,  4.07970918156066, 0.0
        cls._I         = 5.09977122822122, 34.08506759985616, 0.0
        cls._cog       = 2.20637532613114,  0.0
    
    
    def test_check_dimensions(self):
    	self.assertRaises(ValueError, self.section.set_dimensions, r=-1)
    	self.assertRaises(ValueError, self.section.set_dimensions, r=0)
    	self.assertRaises(ValueError, self.section.set_dimensions, phi=-1)
    	self.assertRaises(ValueError, self.section.set_dimensions, phi=0)
    	self.assertRaises(ValueError, self.section.set_dimensions, phi=pi)
    	self.assertRaises(ValueError, self.section.set_dimensions, phi=2*pi)
    	try:
    	    self.section.set_dimensions(phi=0.5*pi)
    	    self.section.set_dimensions(phi=1.5*pi)
    	except:
    	    self.fail("Failed to set legal values of phi")


class TestPhysicalProperties2(TestPhysicalProperties1):
#class TestPhysicalProperties2():
    
    @classmethod
    def setUpClass(cls):
        cls.sectclass  = BaseFillet
        cls.dimensions = dict(r=3.0, phi=pi*5.0/3.0)
        cls.angular    = ["phi"]
        cls.rp         = 5.0, 4.0

        cls.A          = -6.16367930735052
        cls._I0        = -5.09977122822122,  -4.07970918156066, 0.0
        cls._I         = -5.09977122822122, -34.08506759985616, 0.0
        cls._cog       = -2.20637532613114,  0.0


if __name__ == "__main__":
    unittest.main()
