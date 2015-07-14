import unittest

from sections.core import Dimensions


class DimensionsTests(unittest.TestCase):


    def test_init_only_accepts_keyword_arguments(self):
        self.assertRaises(TypeError, Dimensions, 1)
        Dimensions(a=1)


    def test_creates_attributes_from_keywords_to_init(self):
        dims = Dimensions(some_attribute=1)
        
        self.assertTrue(hasattr(dims, "some_attribute"))


    def test_does_not_allow_to_set_new_attributes(self):
        dims = Dimensions()
        
        self.assertRaises(AttributeError, setattr, dims, "a", 1)
    
    
    def test_setting_dimensions(self):
        dims = Dimensions(a=1)
        
        self.assertRaises(TypeError, setattr, dims, "a", bool)
        self.assertRaises(TypeError, setattr, dims, "a", "1")
        
        # The following assignments must work
        dims.a = 1
        dims.a = 1.0
        dims.a = None
    

    def test_raise_value_error_on_getting_dimension_equal_to_None(self):
        dims = Dimensions(a=1)
        dims.a = None
        
        self.assertRaises(ValueError, getattr, dims, "a")
        
    
    def test_dimensions_are_always_float(self):
        dims = Dimensions(a=None, b=None)
        dims.a = 1
        dims.b = 2.0
        
        self.assertIsInstance(dims.a, float)
        self.assertIsInstance(dims.b, float)
    
    
        
        
        
