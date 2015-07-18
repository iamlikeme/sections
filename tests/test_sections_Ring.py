import unittest
import sys

sys.path.insert(0, "..")
from sections.sections import Ring
import test_sections_generic as generic


class TestPhysicalProperties(generic.TestPhysicalProperties, unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.sectclass  = Ring
        cls.dimensions = {"ro":5.0, "ri":3.0}
        cls.rp         = 5.0, 4.0
        cls.A          = 50.26548245743669
        cls._I0        = 427.2566008882119, 427.2566008882119, 0.0
        cls._I         = 427.2566008882119, 427.2566008882119, 0.0
        cls._cog       = 0.0, 0.0
    
    
    def test_check_dimensions(self):
    	self.assertRaises(ValueError, self.section.set_dimensions, ro=-1)
    	self.assertRaises(ValueError, self.section.set_dimensions, ro=0)
    	self.assertRaises(ValueError, self.section.set_dimensions, ri=-1)
    	self.assertRaises(ValueError, self.section.set_dimensions, ri=0)
    	self.assertRaises(ValueError, self.section.set_dimensions, ro=1, ri=2)


if __name__ == "__main__":
    unittest.main()
