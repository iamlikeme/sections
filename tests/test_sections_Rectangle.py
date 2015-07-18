import unittest
import sys

sys.path.insert(0, "..")
from sections.sections import Rectangle
import test_sections_generic as generic


class TestPhysicalProperties(generic.TestPhysicalProperties, unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.sectclass  = Rectangle
        cls.dimensions = {"a":2.0, "b":3.0}
        cls.rp         = 5.0, 4.0
        cls.A          = 6.0
        cls._I0        = 4.5, 2.0, 0.0
        cls._I         = 4.5, 2.0, 0.0
        cls._cog       = 0.0, 0.0
        
    
    def test_check_dimensions(self):
    	self.assertRaises(ValueError, self.section.set_dimensions, a=-1)
    	self.assertRaises(ValueError, self.section.set_dimensions, b=-1)
    	self.assertRaises(ValueError, self.section.set_dimensions, a=0)
    	self.assertRaises(ValueError, self.section.set_dimensions, b=0)
    	
    	
if __name__ == "__main__":
    unittest.main()
