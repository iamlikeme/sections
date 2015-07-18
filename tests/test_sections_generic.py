from math import pi


class TestPhysicalProperties(object):
    """
    Defines tests that should be run for subclasses of SimpleSection and
    ComplexSection.
    """
    
    @classmethod
    def setUpClass(cls):
    	"""
    	Defines known values of physical properties that a section will
    	be checked against. Provide values with at least 7 decimal digits
    	accuracy (so they pass assertAlmostEqual)"""

        cls.sectclass = NotImplemented  # Section class to be checked
        cls.dimensions = NotImplemented  # Dictionary of section dimensions

        # The following physical properties should correspond to cls.dimensions
        cls._cog = NotImplemented  # Position of the cog in local csys
        cls.A    = NotImplemented  # Surface area
        cls._I0  = NotImplemented  # Moments of inertia in local csys moved to cog
        cls._I   = NotImplemented  # Moments of inertia in local csys
        
        # Position of the reference point (rp below) is used to test
        # set_position method. Specify rp coordinates which are of the
        # same order of magnitude as the linear dimensions of the section
        rp       = NotImplemented
    
    
    def setUp(self):
        self.section = self.get_section()
        
    
    def get_section(self, density=1.0):
        """
        A shortcut function to create a section with predefined dimensions."""
        kwargs = {"density" : density}
        kwargs.update(self.dimensions)
        return self.sectclass(**kwargs)
    
        
    def scaled_dimensions(self, factor):
        """
        Returns a copy of self.dimensions whith all values multiplied by
        *factor*. It may be necessary to override this method if some of
        the dimensions are linear (only linear dimensions should be scaled)."""
        return {k:factor*v for k,v in self.dimensions.items()}
    
    
    def test_check_dimensions(self):
    	"""
    	To be implemented in subclass."""
    	raise NotImplementedError
    

    def test_properties_in_local_csys(self):
        
        self.assertAlmostEqual(self.section.A, self.A)
        self.assertAlmostEqual(self.section._cog[0], self._cog[0])
        self.assertAlmostEqual(self.section._cog[1], self._cog[1])
        self.assertAlmostEqual(self.section._I0[0],  self._I0[0])
        self.assertAlmostEqual(self.section._I0[1],  self._I0[1])
        self.assertAlmostEqual(self.section._I0[2],  self._I0[2])
        self.assertAlmostEqual(self.section._I[0],   self._I[0])
        self.assertAlmostEqual(self.section._I[1],   self._I[1])
        self.assertAlmostEqual(self.section._I[2],   self._I[2])


    def test_properties_change_on_density_change(self):
        self.section = self.get_section(density=2.0)
        
        # Position of cog should be independent on density
        # Other properties should change proportionally with density
        
        self.assertAlmostEqual(self.section.A, 2*self.A)
        self.assertAlmostEqual(self.section._cog[0], self._cog[0])
        self.assertAlmostEqual(self.section._cog[1], self._cog[1])
        self.assertAlmostEqual(self.section._I0[0], 2*self._I0[0])
        self.assertAlmostEqual(self.section._I0[1], 2*self._I0[1])
        self.assertAlmostEqual(self.section._I0[2], 2*self._I0[2])
        self.assertAlmostEqual(self.section._I[0],  2*self._I[0])
        self.assertAlmostEqual(self.section._I[1],  2*self._I[1])
        self.assertAlmostEqual(self.section._I[2],  2*self._I[2])
        
        self.section.set_density(-3)
        
        self.assertAlmostEqual(self.section.A, -3*self.A)
        self.assertAlmostEqual(self.section._cog[0], self._cog[0])
        self.assertAlmostEqual(self.section._cog[1], self._cog[1])
        self.assertAlmostEqual(self.section._I0[0], -3*self._I0[0])
        self.assertAlmostEqual(self.section._I0[1], -3*self._I0[1])
        self.assertAlmostEqual(self.section._I0[2], -3*self._I0[2])
        self.assertAlmostEqual(self.section._I[0],  -3*self._I[0])
        self.assertAlmostEqual(self.section._I[1],  -3*self._I[1])
        self.assertAlmostEqual(self.section._I[2],  -3*self._I[2])


    def test_properties_change_on_position_change(self):
        
        # Check rotation without offset
        # =============================
        self.section.set_position(d1=0.0, d2=0.0, theta=pi/2)
        
        # Properties in the local csys should not change
        # ----------------------------------------------
        self.assertEqual(self.section.A,   self.A)
        self.assertEqual(self.section._I0, self._I0)
        self.assertEqual(self.section._I,  self._I)
        
        # Properties in the global csys should change
        # -------------------------------------------
        # The diagonal moments of inertia (I11, I22) should be swapped
        # The product moment of inertia (I12) should change sign
        self.assertAlmostEqual(self.section.I0[0],  self._I0[1])
        self.assertAlmostEqual(self.section.I0[1],  self._I0[0])
        self.assertAlmostEqual(self.section.I0[2], -self._I0[2])        
        self.assertAlmostEqual(self.section.I[0],   self._I[1])
        self.assertAlmostEqual(self.section.I[1],   self._I[0])
        self.assertAlmostEqual(self.section.I[2],  -self._I[2])

        # Check offset with no rotation
        # =============================        
        self.section.set_position(d1=self.rp[0], d2=self.rp[1], theta=0)
        
        # Calculate position of the cog in global csys
        e1 = self.rp[0] + self._cog[0]
        e2 = self.rp[1] + self._cog[1]

        # Properties in the local csys should not change
        # ----------------------------------------------
        self.assertEqual(self.section.A, self.A)
        self.assertEqual(self.section._I0, self._I0)
        self.assertEqual(self.section._I, self._I)
        
        # There is no rotation (theta=0) so I0 and _I0 should be equal
        # ------------------------------------------------------------
        self.assertAlmostEqual(self.section.I0[0], self._I0[0])
        self.assertAlmostEqual(self.section.I0[1], self._I0[1])
        self.assertAlmostEqual(self.section.I0[2], self._I0[2])
        
        # Check moments of inertia about the global axes
        # based on the parallel axis theorem
        # ----------------------------------------------
        self.assertAlmostEqual(self.section.I[0], self._I0[0] + self.A * e2**2)
        self.assertAlmostEqual(self.section.I[1], self._I0[1] + self.A * e1**2)
        self.assertAlmostEqual(self.section.I[2], self._I0[2] + self.A * e1*e2)


    def test_properties_change_on_dimensions_change(self):
        # Evaluate properties in the initial state
        # (to check that cached properties are reset on dimensions change)
        self.section.A
        self.section._I0
        self.section._I

        # Change linear dimensions
        scale = 2.0
        self.section.set_dimensions(**self.scaled_dimensions(scale))
        
        # Expected properties after change of dimensions
        A   = self.A * scale**2
        _I0 = tuple(scale**4*i for i in self._I0)
        _I  = tuple(scale**4*i for i in self._I)
        
        self.assertAlmostEqual(self.section.A, A)
        self.assertAlmostEqual(self.section._I0[0], _I0[0])
        self.assertAlmostEqual(self.section._I0[1], _I0[1])
        self.assertAlmostEqual(self.section._I0[2], _I0[2])
        self.assertAlmostEqual(self.section._I[0], _I[0])
        self.assertAlmostEqual(self.section._I[1], _I[1])
        self.assertAlmostEqual(self.section._I[2], _I[2])
            
    
