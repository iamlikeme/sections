from core import SimpleSection, Dimensions

# ==============================================================================
# S I M P L E   S E C T I O N S
# ==============================================================================


class Rectangle(SimpleSection):
    dimensions = Dimensions(a=None, b=None)
    
    @property
    def A(self):
        return self.density * self.a * self.b
