from math import sin, cos, pi

from core import SimpleSection, ComplexSection, Dimensions, cached_property

# ==============================================================================
# S I M P L E   S E C T I O N S
# ==============================================================================


class Rectangle(SimpleSection):
    dimensions = Dimensions(a=None, b=None)
    
    
    def check_dimensions(self, dims):
        if dims.a <= 0:
            raise ValueError("Invalid dimensions: a <= 0")
        if dims.b <= 0:
            raise ValueError("Invalid dimensions: b <= 0")
        
    
    @cached_property
    def A(self):
        return self.density * self.a * self.b
    

    @cached_property
    def _cog(self):
        return 0.0, 0.0
    
    
    @cached_property
    def _I0(self):
        _I11 = self.a * self.b**3 / 12.
        _I22 = self.b * self.a**3 / 12.
        _I12 = 0.0
        return tuple(self.density * i for i in (_I11, _I22, _I12))



class CircularSector(SimpleSection):
    dimensions = Dimensions(ro=None, ri=None, phi=None)


    def check_dimensions(self, dims):
        if dims.ri < 0:
            raise ValueError("Invalid dimensions: ri < 0")
        if dims.ro <= dims.ri:
            raise ValueError("Invalid dimensions: ro < ri")
        if dims.phi <= 0:
            raise ValueError("Invalid dimensions: phi <= 0")
        if dims.phi > 2*pi:
            raise ValueError("Invalid dimensions: phi > 2*pi")
        

    @cached_property
    def A(self):
        ro  = self.ro
        ri  = self.ri
        phi = self.phi
        A   = 0.5 * (ro**2 - ri**2) * self.phi
        return self.density * A

    
    @cached_property
    def _cog(self):
        ro  = self.ro
        ri  = self.ri
        phi = self.phi
        A   = self.A / self.density
        S2 = 2./3. * (ro**3 - ri**3) * sin(0.5*phi)
        _e1 = S2 / A
        _e2 = 0.0
        return _e1, _e2


    @cached_property
    def _I0(self):
        ro  = self.ro
        ri  = self.ri
        phi = self.phi
        _e1, _e2 = self._cog
        _I11 = self.density * 0.125 * (ro**4 - ri**4) * (phi - sin(phi))
        _I22 = self.density * 0.125 * (ro**4 - ri**4) * (phi + sin(phi))
        _I12 = self.density * 0.0
        return self.parallel_axis((_I11, _I22, _I12), self._cog, reverse=True)



class Polygon(SimpleSection, list):
    

    @cached_property
    def A(self):
        if len(self) < 3:
            raise ValueError("Cannot calculate A: Polygon must have at least three vertices")

        #Area will be positive if vertices are ordered counter-clockwise
        x1, x2 = self.__looped_vertices()
        n = len(self)
        A = 0.5 * sum(x1[i]*x2[i+1] - x1[i+1]*x2[i] for i in range(n))
        return self.density * A
    
    
    @cached_property
    def _cog(self):
        if len(self) < 3:
            raise ValueError("Cannot calculate _cog: Polygon must have at least three vertices")

        x1, x2 = self.__looped_vertices()
        n = len(self)
        A = self.A / self.density
        _e1 = 1. / (6 * A) * sum( (x1[i] + x1[i+1]) * (x1[i]*x2[i+1] - x1[i+1]*x2[i]) for i in range(n) )
        _e2 = 1. / (6 * A) * sum( (x2[i] + x2[i+1]) * (x1[i]*x2[i+1] - x1[i+1]*x2[i]) for i in range(n) )
        return _e1, _e2
            
            
    @cached_property
    def _I0(self):
        if len(self) < 3:
            raise ValueError("Cannot calculate _I0: Polygon must have at least three vertices")
        
        x1, x2 = self.__looped_vertices()
        n = len(self)
        _I11 = 1./12. * sum( (x2[i]**2 + x2[i]*x2[i+1] + x2[i+1]**2) * (x1[i]*x2[i+1] - x1[i+1]*x2[i]) for i in range(n))
        _I22 = 1./12. * sum( (x1[i]**2 + x1[i]*x1[i+1] + x1[i+1]**2) * (x1[i]*x2[i+1] - x1[i+1]*x2[i]) for i in range(n))
        _I12 = 1./24. * sum( (x1[i]*x2[i+1] + 2*x1[i]*x2[i] + 2*x1[i+1]*x2[i+1] + x1[i+1]*x2[i] )*(x1[i]*x2[i+1] - x1[i+1]*x2[i]) for i in range(n))

        _I = tuple(self.density * i for i in (_I11, _I22, _I12))
        return self.parallel_axis(_I, self._cog, reverse=True)

    
    def __looped_vertices(self):
        n = len(self)
        x1 = [self[i%n][0] for i in range(n + 1)]
        x2 = [self[i%n][1] for i in range(n + 1)]
        return x1, x2

    
    # Override list methods which add new items to the list
    # Only allow to add items consisting of two values which can be
    # convered to float.
    # Any change of vertices must call self.reset_cached_properties
    # =============================================================
    
    def append(self, vertex):
        vertex = self.__convert_to_vertices(vertex)[0]
        list.append(self, vertex)
        self.reset_cached_properties()
    

    def extend(self, vertices):
        vertices = self.__convert_to_vertices(*vertices)
        list.extend(self, vertices)
        self.reset_cached_properties()
        
    
    def insert(self, i, vertex):
        vertex = self.__convert_to_vertices(vertex)[0]
        list.insert(self, i, vertex)
        self.reset_cached_properties()
        
    
    def __setitem__(self, i, vertex):
        vertex = self.__convert_to_vertices(vertex)[0]
        list.__setitem__(self, i, vertex)
        self.reset_cached_properties()
    
    
    def __setslice__(self, i, j, vertices):
        vertices = self.__convert_to_vertices(*vertices)
        list.__setslice__(self, i, j, vertices)
        self.reset_cached_properties()
                
    
    def __convert_to_vertices(self, *items):
        return [(float(x), float(y)) for x, y in items]
            
    # =============================================================




# ==============================================================================
# C O M P L E X   S E C T I O N S
# ==============================================================================

class Circle(ComplexSection):
    dimensions = Dimensions(r=None)
    sections   = [CircularSector]
    
    
    def update_sections(self):
        self.sections[0].set_dimensions(ri=0, ro=self.r, phi=2*pi)
    

