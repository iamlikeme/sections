import unittest
from math import pi

from sections.core import BaseSection, Dimensions, cached_property


class BaseSectionTests(unittest.TestCase):

    def test_initial_state(self):
        section = BaseSection()
        
        self.assertEqual(section.density, 1.0)
        self.assertEqual(section.position, (0.0, 0.0, 0.0))
        self.assertIsInstance(section.dimensions, Dimensions)
    
    
    def test_setting_density(self):
        section = BaseSection(density=2)
        
        self.assertRaises(AttributeError, setattr, section, "density", 3.0)
        self.assertEqual(section.density, 2.0)
        self.assertIsInstance(section.density, float)
        
        self.assertRaises(ValueError, section.set_density, "abc")
        self.assertRaises(ValueError, section.set_density, 0.0)

        section.set_density(3)
        self.assertEqual(section.density, 3.0)
        self.assertIsInstance(section.density, float)
        
    
    def test_setting_position(self):
        section = BaseSection()
        
        self.assertRaises(AttributeError, setattr, section, "position", (0, 0, 0))
        
        section.set_position(d1=1)
        self.assertIsInstance(section.position[0], float)
        self.assertEqual(section.position, (1.0, 0.0, 0.0))

        section.set_position(d2=2)
        self.assertIsInstance(section.position[1], float)
        self.assertEqual(section.position, (1.0, 2.0, 0.0))
        
        section.set_position(theta=3)
        self.assertIsInstance(section.position[2], float)
        self.assertEqual(section.position, (1.0, 2.0, 3.0))
        
        section.set_position(4, 5, 6)
        self.assertEqual(section.position, (4.0, 5.0, 6.0))
    
    
    def test_initializing_dimensions(self):
        class Dummy(BaseSection):
            dimensions = Dimensions(dim_a=5, dim_b=None)
        section1 = Dummy()
        section2 = Dummy(dim_a=3, dim_b=4)
        
        self.assertEqual(section1.dim_a, 5.0)
        self.assertRaises(ValueError, getattr, section1, "dim_b")
        
        self.assertEqual(section2.dim_a, 3.0)
        self.assertEqual(section2.dim_b, 4.0)
        self.assertIsInstance(section2.dim_a, float)
        self.assertIsInstance(section2.dim_b, float)
        
    
    def test_setting_dimensions(self):
        class Dummy(BaseSection):
            dimensions = Dimensions(dim_a=None, dim_b=None)

        section = Dummy()
        section.set_dimensions(dim_a=3, dim_b=4)

        self.assertEqual(section.dim_a, 3.0)
        self.assertEqual(section.dim_b, 4.0)
        self.assertIsInstance(section.dim_a, float)
        self.assertIsInstance(section.dim_b, float)
        self.assertRaises(AttributeError, setattr, section, "dim_a", 5)
        self.assertRaises(TypeError, section.set_dimensions, dim_a="abc")
        
        try:
            section.set_dimensions(dim_a="abc", dim_b=7)
        except:
            self.assertEqual(section.dim_a, 3.0)
            self.assertEqual(section.dim_b, 4.0)
        
        
    def test_delegating_dimensions(self):
        class Dummy(BaseSection):
            dimensions = Dimensions(dim_a=None, dim_b=None)
        section = Dummy()
        
        section.set_dimensions(dim_a=5, dim_b=6)
        self.assertEqual(section.dim_a, section.dimensions.dim_a)
        self.assertEqual(section.dim_b, section.dimensions.dim_b)
    

    def test_set_dimensions_calls_check_dimensions(self):
        def error_raiser(dims):
            raise ValueError
        section = BaseSection()
        section.check_dimensions = error_raiser
            
        self.assertRaises(ValueError, section.set_dimensions)    	


    def test_cached_properties(self):
        self.assertTrue(isinstance(BaseSection._cog, cached_property))
        self.assertTrue(isinstance(BaseSection.cog, cached_property))
        self.assertTrue(isinstance(BaseSection.A, cached_property))
        self.assertTrue(isinstance(BaseSection._I0, cached_property))
        self.assertTrue(isinstance(BaseSection._I, cached_property))
        self.assertTrue(isinstance(BaseSection.I0, cached_property))
        self.assertTrue(isinstance(BaseSection.I, cached_property))        

    
    def test_reset_cached_properties(self):
        # BaseSection.reset_cached_properties should be called when changing
        # dimensions, density or position
        
        # It should be also checked that cached properties are deleted by
        # reset_cached_properties. This is checked only for subclasses

        def error_raiser():
            raise ValueError
        section = BaseSection()
        section.reset_cached_properties = error_raiser
    	
    	self.assertRaises(ValueError, section.set_dimensions)
    	self.assertRaises(ValueError, section.set_density, 2)
    	self.assertRaises(ValueError, section.set_position, 1, 2, 3)


    def test_vector_transformation(self):
        section = BaseSection()
        v1 = (2.0, 3.0)
        v2 = (0.0, 0.0)
        
        section.set_position(d1=-2.0, d2=0.0, theta=0.0)
        self.assertEqual(section.transform_to_global(v1), (0.0, 3.0))
        self.assertEqual(section.transform_to_global(v2), (-2.0, 0.0))
        
        section.set_position(d1=0.0, d2=-3.0, theta=0.0)
        self.assertEqual(section.transform_to_global(v1), (2.0, 0.0))
        self.assertEqual(section.transform_to_global(v2), (0.0, -3.0))
        
        section.set_position(d1=0.0, d2=0.0, theta=pi/2)
        self.assertAlmostEqual(section.transform_to_global(v1)[0], -3.0)
        self.assertAlmostEqual(section.transform_to_global(v1)[1], 2.0)
        self.assertAlmostEqual(section.transform_to_global(v2)[0], 0.0)
        self.assertAlmostEqual(section.transform_to_global(v2)[1], 0.0)
        
        section.set_position(d1=3.0, d2=-2.0, theta=pi/2)
        self.assertAlmostEqual(section.transform_to_global(v1)[0], 0.0)
        self.assertAlmostEqual(section.transform_to_global(v1)[1], 0.0)
        self.assertAlmostEqual(section.transform_to_global(v2)[0], 3.0)
        self.assertAlmostEqual(section.transform_to_global(v2)[1], -2.0)
        
    
    
    def test_symmetric_matrix_transformation(self):
        # Symmetric matrix is defined by (m11, m22, m12)
        # Position of the origin should have no influence on matrix components
        # Transformation should only depend on rotation of the section 

        section = BaseSection()
        m1 = (1.0, 1.0, 0.0)
        m2 = (1.0, 2.0, 3.0)

        section.set_position(d1=2.0, d2=0.0, theta=0.0)
        self.assertEqual(section.transform_to_global(m1), m1)
        self.assertEqual(section.transform_to_global(m2), m2)
        
        section.set_position(d1=0.0, d2=3.0, theta=0.0)
        self.assertEqual(section.transform_to_global(m1), m1)
        self.assertEqual(section.transform_to_global(m2), m2)
        
        section.set_position(d1=0.0, d2=0.0, theta=pi/2)
        self.assertAlmostEqual(section.transform_to_global(m1)[0], 1.0)
        self.assertAlmostEqual(section.transform_to_global(m1)[1], 1.0)
        self.assertAlmostEqual(section.transform_to_global(m1)[2], 0.0)
        self.assertAlmostEqual(section.transform_to_global(m2)[0], 2.0)
        self.assertAlmostEqual(section.transform_to_global(m2)[1], 1.0)
        self.assertAlmostEqual(section.transform_to_global(m2)[2], -3.0)

    
    def test_centre_of_gravity(self):
        _cog = (2.0, 3.0)
        class Dummy(BaseSection):
            @property
            def _cog(self):
                return _cog
        section = Dummy()
        
        self.assertEqual(section._cog, section.cog)
        
        section.set_position(d1=5.0, d2=0.0, theta=0.0)
        self.assertEqual(section.cog, (7.0, 3.0))
        
        section.set_position(d1=0.0, d2=5.0, theta=0.0)
        self.assertEqual(section.cog, (2.0, 8.0))
        
        section.set_position(d1=0.0, d2=0.0, theta=pi/2)
        self.assertAlmostEqual(section.cog[0], -_cog[1])
        self.assertAlmostEqual(section.cog[1], _cog[0])

        cog = section.cog
        section.set_density(2)
        self.assertEqual(section.cog, cog)
    

