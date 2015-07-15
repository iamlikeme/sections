import unittest
from math import pi

from sections.sections import Rectangle
from sections.core import SimpleSection


class RectangleTests(unittest.TestCase):
    
    def setUp(self):
        self.a    = 2.0
        self.b    = 3.0
        self._cog = 0.0, 0.0
        self.A    = self.a * self.b
        self._I0  = self.a * self.b**3 / 12., \
                    self.b * self.a**3 / 12., \
                    0.0
        self._I   = self._I0
        self.rp   = 0.5*self.b, 0.5*self.a

    
    def test_properties_in_local_csys(self):
        rec  = Rectangle(a=self.a, b=self.b)
        
        self.assertEqual(rec.A, self.A)
        self.assertEqual(rec._cog, self._cog)
        self.assertEqual(rec._I0, self._I0)
        self.assertEqual(rec._I, self._I)
        
    
    def test_density(self):
        rec  = Rectangle(a=self.a, b=self.b, density=2)

        self.assertEqual(rec._cog, self._cog)
        self.assertEqual(rec.A, 2*self.A)
        self.assertEqual(rec._I0, tuple(2*i for i in self._I0))
        self.assertEqual(rec._I, tuple(2*i for i in self._I))
        
        rec.set_density(-3)
        self.assertEqual(rec._cog, self._cog)
        self.assertEqual(rec.A, -3*self.A)
        self.assertEqual(rec._I0, tuple(-3*i for i in self._I0))
        self.assertEqual(rec._I, tuple(-3*i for i in self._I))
    
    
    def test_position(self):
        rec  = Rectangle(a=self.a, b=self.b)
        
        # Check rotation without offset
        # =============================
        rec.set_position(d1=0.0, d2=0.0, theta=pi/2)
        
        # Properties in the local csys should not change
        self.assertEqual(rec.A, self.A)
        self.assertEqual(rec._I0, self._I0)
        self.assertEqual(rec._I, self._I)
        
        # The diagonal moments of inertia (I11, I22) should switch places
        self.assertAlmostEqual(rec.I0[0], self._I0[1])
        self.assertAlmostEqual(rec.I0[1], self._I0[0])
        self.assertAlmostEqual(rec.I0[2], self._I0[2])
        
        # The diagonal moments of inertia (I11, I22) should switch places
        self.assertAlmostEqual(rec.I[0], self._I[1])
        self.assertAlmostEqual(rec.I[1], self._I[0])
        self.assertAlmostEqual(rec.I[2], self._I[2])

        # Check offset with no rotation
        # =============================        
        rec.set_position(d1=self.rp[0], d2=self.rp[1], theta=0)

        # Properties in the local csys should not change
        self.assertEqual(rec.A, self.A)
        self.assertEqual(rec._I0, self._I0)
        self.assertEqual(rec._I, self._I)
        
        # There is no rotation (theta=0) so I0 and _I0 should be equal
        self.assertAlmostEqual(rec.I0[0], self._I0[0])
        self.assertAlmostEqual(rec.I0[1], self._I0[1])
        self.assertAlmostEqual(rec.I0[2], self._I0[2])
        
        # Check parallel axis theorem
        self.assertAlmostEqual(rec.I[0], self._I[0] + self.A * self.rp[1]**2)
        self.assertAlmostEqual(rec.I[1], self._I[1] + self.A * self.rp[0]**2)
        self.assertAlmostEqual(rec.I[2], self._I[2] + self.A * self.rp[0]*self.rp[1])
        
    
    def test_dimensions(self):
        rec  = Rectangle(a=self.a, b=self.b)
        # Evaluate properties
        rec.A
        rec._I0
        rec._I
        
        # Check if properties change when dimensions are changed
        rec.set_dimensions(a=2*self.a, b=2*self.b)
        self.assertEqual(rec.A, 4*self.A)
        self.assertEqual(rec._I0, tuple(16*i for i in self._I0))
        self.assertEqual(rec._I, tuple(16*i for i in self._I))
        
