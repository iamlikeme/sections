import unittest
from math import pi

from sections.sections import CircularSector
from tests.test_section import SectionTests

class CircularSectorTests(unittest.TestCase, SectionTests):
    
    def setUp(self):
        self.cls        = CircularSector
        self.ro         = 5.0
        self.ri         = 0.0
        self.phi        = pi/3
        self.dimensions = {"ro":self.ro, "ri":self.ri, "phi":self.phi}
        self.rp         = 3.0, 4.0
        self.A          = 13.08996938995747
        self._I         = 14.154074016574924, 149.47054335789346, 0.0
        self._I0        = 14.154074016574924, 16.841424114647396, 0.0
        self._cog       = 3.183098861837906, 0.0
    
    
    def scaled_dimensions(self, factor):
    	return {"ro":factor*self.ro, "ri":factor*self.ri}


class CircularSectorTests2(unittest.TestCase):
    
    def test_todo(self):
        self.fail("TODO: Add tests for circular sector with ri>0")
