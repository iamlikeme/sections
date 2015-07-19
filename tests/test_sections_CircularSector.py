import unittest
import sys
from math import pi

sys.path.insert(0, "..")
from sections.sections import CircularSector
import test_sections_generic as generic


class TestPhysicalProperties1(generic.TestPhysicalProperties, unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.sectclass  = CircularSector
        cls.dimensions = dict(ro=5.0, ri=0.0, phi=pi/3)
        cls.angular    = ["phi"]
        cls.rp         = 3.0, 4.0
        cls.A          = 13.08996938995747
        cls._I         = 14.154074016574924, 149.47054335789346, 0.0
        cls._I0        = 14.154074016574924, 16.841424114647396, 0.0
        cls._cog       = 3.183098861837906, 0.0
    
    
    def test_check_dimensions(self):
    	self.assertRaises(ValueError, self.section.set_dimensions, ri=-1)
    	self.assertRaises(ValueError, self.section.set_dimensions, ro=-1)
    	self.assertRaises(ValueError, self.section.set_dimensions, ro= 0)
    	self.assertRaises(ValueError, self.section.set_dimensions, ro=1, ri=2)
    	self.assertRaises(ValueError, self.section.set_dimensions, phi=-0.1*pi)
    	self.assertRaises(ValueError, self.section.set_dimensions, phi=0)
    	self.assertRaises(ValueError, self.section.set_dimensions, phi=2.1 * pi)
    
    

class TestPhysicalProperties2(TestPhysicalProperties1):
    
    @classmethod
    def setUpClass(cls):
        cls.sectclass  = CircularSector
        cls.dimensions = dict(ro=5.0, ri=3.0, phi=pi)
        cls.angular    = ["phi"]
        cls.rp         = 5.0, 4.0
        cls._cog       = 2.599530737167624, 0.0
        cls.A          = 25.132741228718345
        cls._I0        = 213.62830044410595, 43.792292282487864, 0.0
        cls._I         = 213.62830044410595, 213.62830044410595, 0.0

    

if __name__ == "__main__":
    unittest.main()
