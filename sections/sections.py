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
        
