import unittest
import sys
from math import pi

sys.path.insert(0, "..")
from sections.sections import Wedge
import test_sections_generic as generic


class TestPhysicalProperties(generic.TestPhysicalProperties, unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.sectclass  = Wedge
        cls.dimensions = dict(r=3.0, phi=pi)
        cls.angular    = ["phi"]
        cls.rp         = 5.0, 4.0
        cls._cog       = 1.2732395447351625, 0.0
        cls.A          = 14.137166941154069
        cls._I0        = 31.808625617596654, 8.890313812363729, 0.0
        cls._I         = 31.808625617596654, 31.808625617596654, 0.0
    
        
    def test_check_dimensions(self):
    	self.assertRaises(ValueError, self.section.set_dimensions, r=-1)
    	self.assertRaises(ValueError, self.section.set_dimensions, r=0)
    	self.assertRaises(ValueError, self.section.set_dimensions, phi=-1)
    	self.assertRaises(ValueError, self.section.set_dimensions, phi=0)
    	self.assertRaises(ValueError, self.section.set_dimensions, phi=2.1*pi)



if __name__ == "__main__":
    unittest.main()
