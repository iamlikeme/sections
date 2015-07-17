import unittest
from math import pi


class SectionTests(object):
    """
    Defines tests that should be run for subclasses of SimpleSection and
    ComplexSection.
    """
    
    # The following values should be set in a subclass (or in its setUp method)
    # Provide values with at least 7 decimal digits accuracy (so they pass
    # assertAlmostEqual)
    cls        = NotImplemented  # Section class to be checked
    dimensions = NotImplemented  # Should be a dict
    rp         = NotImplemented  # Position of the reference point
    A          = NotImplemented  # Surface area
    _I0        = NotImplemented  # Moments of inertia in local csys moved to cog
    _I         = NotImplemented  # Moments of inertia in local csys
    _cog       = NotImplemented  # Position of the cog in local csys
        
    
    def get_section(self, density=1.0):
        """
        A shortcut function to create a section with predefined dimensions."""
        kwargs = {"density" : density}
        kwargs.update(self.dimensions)
        return self.cls(**kwargs)
    
    
    def scaled_dimensions(self, factor):
        return {k:factor*v for k,v in self.dimensions.items()}
    

    def test_properties_in_local_csys(self):
        sec = self.get_section()
        
        self.assertAlmostEqual(sec.A, self.A)
        self.assertAlmostEqual(sec._cog[0], self._cog[0])
        self.assertAlmostEqual(sec._cog[1], self._cog[1])
        self.assertAlmostEqual(sec._I0[0], self._I0[0])
        self.assertAlmostEqual(sec._I0[1], self._I0[1])
        self.assertAlmostEqual(sec._I0[2], self._I0[2])
        self.assertAlmostEqual(sec._I[0], self._I[0])
        self.assertAlmostEqual(sec._I[1], self._I[1])
        self.assertAlmostEqual(sec._I[2], self._I[2])


    def test_density(self):
        sec = self.get_section(density=2.0)

        self.assertAlmostEqual(sec._cog[0], self._cog[0])
        self.assertAlmostEqual(sec._cog[1], self._cog[1])
        self.assertAlmostEqual(sec.A, 2*self.A)
        self.assertAlmostEqual(sec._I0[0], 2*self._I0[0])
        self.assertAlmostEqual(sec._I0[1], 2*self._I0[1])
        self.assertAlmostEqual(sec._I0[2], 2*self._I0[2])
        self.assertAlmostEqual(sec._I[0], 2*self._I[0])
        self.assertAlmostEqual(sec._I[1], 2*self._I[1])
        self.assertAlmostEqual(sec._I[2], 2*self._I[2])
        
        sec.set_density(-3)
        self.assertAlmostEqual(sec._cog[0], self._cog[0])
        self.assertAlmostEqual(sec._cog[1], self._cog[1])
        self.assertAlmostEqual(sec.A, -3*self.A)
        self.assertAlmostEqual(sec._I0[0], -3*self._I0[0])
        self.assertAlmostEqual(sec._I0[1], -3*self._I0[1])
        self.assertAlmostEqual(sec._I0[2], -3*self._I0[2])
        self.assertAlmostEqual(sec._I[0], -3*self._I[0])
        self.assertAlmostEqual(sec._I[1], -3*self._I[1])
        self.assertAlmostEqual(sec._I[2], -3*self._I[2])


    def test_position(self):
        sec = self.get_section()
        
        # Check rotation without offset
        # =============================
        sec.set_position(d1=0.0, d2=0.0, theta=pi/2)
        
        # Properties in the local csys should not change
        self.assertEqual(sec.A, self.A)
        self.assertEqual(sec._I0, self._I0)
        self.assertEqual(sec._I, self._I)
        
        # The diagonal moments of inertia (I11, I22) should switch places
        self.assertAlmostEqual(sec.I0[0], self._I0[1])
        self.assertAlmostEqual(sec.I0[1], self._I0[0])
        self.assertAlmostEqual(sec.I0[2], -self._I0[2])
        
        # The diagonal moments of inertia (I11, I22) should switch places
        self.assertAlmostEqual(sec.I[0], self._I[1])
        self.assertAlmostEqual(sec.I[1], self._I[0])
        self.assertAlmostEqual(sec.I[2], -self._I[2])

        # Check offset with no rotation
        # =============================        
        sec.set_position(d1=self.rp[0], d2=self.rp[1], theta=0)
        e1 = self.rp[0] + self._cog[0]
        e2 = self.rp[1] + self._cog[1]

        # Properties in the local csys should not change
        self.assertEqual(sec.A, self.A)
        self.assertEqual(sec._I0, self._I0)
        self.assertEqual(sec._I, self._I)
        
        # There is no rotation (theta=0) so I0 and _I0 should be equal
        self.assertAlmostEqual(sec.I0[0], self._I0[0])
        self.assertAlmostEqual(sec.I0[1], self._I0[1])
        self.assertAlmostEqual(sec.I0[2], self._I0[2])
        
        # Check parallel axis theorem
        self.assertAlmostEqual(sec.I[0], self._I0[0] + self.A * e2**2)
        self.assertAlmostEqual(sec.I[1], self._I0[1] + self.A * e1**2)
        self.assertAlmostEqual(sec.I[2], self._I0[2] + self.A * e1*e2)


    def test_dimensions(self):
        sec = self.get_section()
        # Evaluate properties
        sec.A
        sec._I0
        sec._I
        
        # Check if properties change when dimensions are changed
        scale = 2.0
        sec.set_dimensions(**self.scaled_dimensions(scale))
        self.assertEqual(sec.A, scale**2 * self.A)
        self.assertEqual(sec._I0, tuple(scale**4*i for i in self._I0))
        self.assertEqual(sec._I, tuple(scale**4*i for i in self._I))
            
    
