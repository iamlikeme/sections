import unittest
import sys

sys.path.insert(0, "..")
from sections.sections import Box
from test_sections import SectionTests


class TestDimensions(unittest.TestCase):
    
    def test_check_dimensions(self):
        box = Box(a=10, b=20, ta=2, tb=1)

        self.assertRaises(ValueError, box.set_dimensions, a=-1)
        self.assertRaises(ValueError, box.set_dimensions, a=0)
        self.assertRaises(ValueError, box.set_dimensions, b=-1)
        self.assertRaises(ValueError, box.set_dimensions, b=0)
        self.assertRaises(ValueError, box.set_dimensions, ta=-1)
        self.assertRaises(ValueError, box.set_dimensions, ta=0)
        self.assertRaises(ValueError, box.set_dimensions, tb=-1)
        self.assertRaises(ValueError, box.set_dimensions, tb=0)
        self.assertRaises(ValueError, box.set_dimensions, a=10, tb=5)
        self.assertRaises(ValueError, box.set_dimensions, b=20, ta=10)


class TestPhysicalProperties(unittest.TestCase, SectionTests):
    
    @classmethod
    def setUpClass(cls):
        cls.cls        = Box
        cls.dimensions = dict(a=10, b=20, ta=2, tb=1)
        cls.rp         = 12.0, 15.0
        cls.A          = 72.0
        cls._I0        = 3936.0, 984.0, 0.0
        cls._I         = 3936.0, 984.0, 0.0
        cls._cog       = 0.0, 0.0
        



if __name__ == "__main__":
    unittest.main()
