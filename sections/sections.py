from math import sin, cos, pi

from core import SimpleSection, Dimensions

# ==============================================================================
# S I M P L E   S E C T I O N S
# ==============================================================================


class Rectangle(SimpleSection):
    dimensions = Dimensions(a=None, b=None)
    
    @property
    def A(self):
        return self.density * self.a * self.b
    

    @property
    def _cog(self):
        return 0.0, 0.0
    
    
    @property
    def _I0(self):
        _I11 = self.a * self.b**3 / 12.
        _I22 = self.b * self.a**3 / 12.
        _I12 = 0.0
        return tuple(self.density * i for i in (_I11, _I22, _I12))



class CircularSector(SimpleSection):
    dimensions = Dimensions(ro=None, ri=None, phi=None)

    @property
    def A(self):
        ro  = self.ro
        ri  = self.ri
        phi = self.phi
        A   = 0.5 * (ro**2 - ri**2) * self.phi
        return self.density * A

    
    @property
    def _cog(self):
        ro  = self.ro
        ri  = self.ri
        phi = self.phi
        A   = self.A / self.density
        S2 = 2./3. * (ro**3 - ri**3) * sin(0.5*phi)
        _e1 = S2 / A
        _e2 = 0.0
        return _e1, _e2


    @property
    def _I0(self):
        ro  = self.ro
        ri  = self.ri
        phi = self.phi
        _e1, _e2 = self._cog
        _I11 = self.density * 0.125 * (ro**4 - ri**4) * (phi - sin(phi))
        _I22 = self.density * 0.125 * (ro**4 - ri**4) * (phi + sin(phi))
        _I12 = self.density * 0.0
        return self.parallel_axis((_I11, _I22, _I12), self._cog, reverse=True)

