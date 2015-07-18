import unittest
import sys

sys.path.insert(0, "..")
from sections.sections import Circle
import test_sections_generic as generic


class TestPhysicalProperties(generic.TestPhysicalProperties, unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.sectclass  = Circle
        cls.dimensions = {"r":3.0}
        cls.rp         = 5.0, 4.0
        cls.A          = 28.274333882308138
        cls._I0        = 63.61725123519331, 63.61725123519331, 0.0
        cls._I         = 63.61725123519331, 63.61725123519331, 0.0
        cls._cog       = 0.0, 0.0
    
    
    def test_check_dimensions(self):
    	self.assertRaises(ValueError, self.section.set_dimensions, r=-1)
    	self.assertRaises(ValueError, self.section.set_dimensions, r=0)


if __name__ == "__main__":
    unittest.main()
