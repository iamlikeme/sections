import unittest

from sections.core import SimpleSection, cached_property


class SimpleSectionTests(unittest.TestCase):
    
    
    def test_cached_properties(self):
        self.assertTrue(isinstance(SimpleSection._cog, cached_property))
        self.assertTrue(isinstance(SimpleSection.cog, cached_property))
        self.assertTrue(isinstance(SimpleSection.A, cached_property))
        self.assertTrue(isinstance(SimpleSection._I0, cached_property))
        self.assertTrue(isinstance(SimpleSection._I, cached_property))
        self.assertTrue(isinstance(SimpleSection.I0, cached_property))
        self.assertTrue(isinstance(SimpleSection.I, cached_property))        
    
    
    def test_reset_cached_properties(self):
        # BaseSection.reset_cached_properties should be called when changing
        # dimensions, density or position
        
        # It should be also checked that cached properties are deleted by
        # reset_cached_properties. This is checked only for subclasses

        def error_raiser():
            raise ValueError
        section = SimpleSection()
        section.reset_cached_properties = error_raiser
    	
    	self.assertRaises(ValueError, section.set_dimensions)
    	self.assertRaises(ValueError, section.set_density, 2)
    	self.assertRaises(ValueError, section.set_position, 1, 2, 3)
