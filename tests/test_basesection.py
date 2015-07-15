import unittest
from math import pi

from sections.core import BaseSection, Dimensions


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
        
    
    
    def test_matrix_transformation(self):
        pass
