import unittest

from sections.sections import Rectangle
from tests.test_section import SectionTests

class RectangleTests(unittest.TestCase, SectionTests):
    
    def setUp(self):
        self.a          = 2.0
        self.b          = 3.0
        self.cls        = Rectangle
        self.dimensions = {"a":self.a, "b":self.b}
        self.rp         = 0.5*self.b, 0.5*self.a
        self.A          = self.a * self.b
        self._I0        = self.a * self.b**3 / 12., \
                          self.b * self.a**3 / 12., \
                          0.0
        self._cog       = 0.0, 0.0
