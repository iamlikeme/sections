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


class CircularSegment(SimpleSection):
    dimensions = Dimensions(r=None, phi=None)


    def check_dimensions(self, dims):
        if dims.r <= 0:
            raise ValueError("Invalid dimensions: r <= 0")
        if dims.phi <= 0:
            raise ValueError("Invalid dimensions: phi <= 0")
        if dims.phi > 2*pi:
            raise ValueError("Invalid dimensions: phi > 0")
        

    @cached_property
    def _cog(self):
        r, phi = self.r, self.phi
        _e1 = 4 * sin(0.5*phi)**3 * r / (3 * (phi - sin(phi)) )
        _e2 = 0.0
        return _e1, _e2
    

    @cached_property
    def A(self):
        r, phi = self.r, self.phi
        return self.density * 0.5 * r**2 * (phi - sin(phi))


    @cached_property
    def _I0(self):
        r   = self.r
        phi = self.phi
        A  = self.A / self.density
        e1, e2 = self._cog
        I11 = 1. / 48. * r**4 * (6*phi - 8*sin(phi) + sin(2*phi))        
        I22 = 0.125 * r**4 * (phi - sin(phi)*cos(phi)) - A * e1**2
        I12 = 0.0
        return tuple(self.density * i for i in (I11, I22, I12))
    



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
        vertex = self.convert_to_vertices(vertex)[0]
        list.append(self, vertex)
        self.reset_cached_properties()
    

    def extend(self, vertices):
        vertices = self.convert_to_vertices(*vertices)
        list.extend(self, vertices)
        self.reset_cached_properties()
        
    
    def insert(self, i, vertex):
        vertex = self.convert_to_vertices(vertex)[0]
        list.insert(self, i, vertex)
        self.reset_cached_properties()
        
    
    def __setitem__(self, i, vertex):
        vertex = self.convert_to_vertices(vertex)[0]
        list.__setitem__(self, i, vertex)
        self.reset_cached_properties()
    
    
    def __setslice__(self, i, j, vertices):
        vertices = self.convert_to_vertices(*vertices)
        list.__setslice__(self, i, j, vertices)
        self.reset_cached_properties()
                
    
    @staticmethod
    def convert_to_vertices(*items):
        return [(float(x), float(y)) for x, y in items]
            
    # =============================================================



class Triangle(Polygon):

    # Override list methods which add new items to the list
    # Only allow to add items consisting of two values which can be
    # convered to float.
    # Any change of vertices must call self.reset_cached_properties
    # =============================================================
    
    def append(self, vertex):
        if len(self) == 3:
            raise IndexError("Triangle cannot have more than 3 vertices")
        super(Triangle, self).append(vertex)
    

    def extend(self, vertices):        
        vertices = self.convert_to_vertices(*vertices)
        if len(self) + len(vertices) > 3:
            raise IndexError("Triangle cannot have more than 3 vertices")
        super(Triangle, self).extend(vertices)
        
    
    def insert(self, i, vertex):
        if len(self) == 3:
            raise IndexError("Triangle cannot have more than 3 vertices")
        super(Triangle, self).insert(i, vertex)
        
    
    def __setslice__(self, i, j, vertices):
        vertices = self.convert_to_vertices(*vertices)
        resulting = self[:]
        resulting.__setslice__(i, j, vertices)
        if len(resulting) > 3:
            raise IndexError("Triangle cannot have more than 3 vertices")        
        super(Triangle, self).__setslice__(i, j, vertices)

                
    # =============================================================
    
    def reset_cached_properties(self):
        
        if len(self) == 3:
            x, y = zip(*self)
            v1 = x[1] - x[0], y[1] - y[0]
            v2 = x[2] - x[1], y[2] - y[1]
            sin = v1[0] * v2[1] - v1[1] * v2[0]
            if sin < 0:
                self[:] = self[0], self[2], self[1]
        super(Triangle, self).reset_cached_properties()
            
            
        



# ==============================================================================
# C O M P L E X   S E C T I O N S
# ==============================================================================

class Circle(ComplexSection):
    dimensions = Dimensions(r=None)
    sections   = [CircularSector]
    
    
    def update_sections(self):
        self.sections[0].set_dimensions(ri=0, ro=self.r, phi=2*pi)
    


class Box(ComplexSection):
    dimensions = Dimensions(a=None, b=None, ta=None, tb=None)
    sections = [Polygon]
    
    
    def check_dimensions(self, dims):
        if dims.a <= 0:
            raise ValueError("Invalid dimensions: a <= 0")
        if dims.b <= 0:
            raise ValueError("Invalid dimensions: b <= 0")
        if dims.ta <= 0:
            raise ValueError("Invalid dimensions: ta <= 0")
        if dims.tb <= 0:
            raise ValueError("Invalid dimensions: tb <= 0")
        if dims.a <= 2*dims.tb:
            raise ValueError("Invalid dimensions: a <= 2*tb")
        if dims.b <= 2*dims.ta:
            raise ValueError("Invalid dimensions: b <= 2*ta")
    
    
    def update_sections(self):
        ao = 0.5 * self.a
        ai = 0.5 * (self.a - 2*self.tb)
        bo = 0.5 * self.b
        bi = 0.5 * (self.b - 2*self.ta)
        
        polygon = self.sections[0]
        polygon[:] = [
            (-ao, -bo),
            ( ao, -bo),
            ( ao,  bo),
            (-ao,  bo),
            (-ao, -bi),
            (-ai, -bi),
            (-ai,  bi),
            ( ai,  bi),
            ( ai, -bi),
            (-ao, -bi)]


class Ring(ComplexSection):
    sections   = [CircularSector]
    dimensions = Dimensions(ro=None, ri=None)
    
    
    def update_sections(self):
        self.sections[0].set_dimensions(ro=self.ro, ri=self.ri, phi=2*pi)
    
    
    def check_dimensions(self, dims):
        super(Ring, self).check_dimensions(dims)



class Wedge(ComplexSection):
    sections   = [CircularSector]
    dimensions = Dimensions(r=None, phi=None)
    
    
    def update_sections(self):
        self.sections[0].set_dimensions(ro=self.r, ri=0, phi=self.phi)
        

class WedgeRing(CircularSector):
    pass


class BaseFillet(ComplexSection):
    sections   = [Triangle, CircularSegment]
    dimensions = Dimensions(r=None, phi=None)
    densities  = [1.0, -1.0]
    
    
    def check_dimensions(self, dims):
        if dims.r <= 0:
            raise ValueError("Invalid dimensions: r <= 0")
        if dims.phi <= 0:
            raise ValueError("Invalid dimensions: phi <= 0")
        if dims.phi == pi:
            raise ValueError("Invalid dimensions: phi = pi")
        if dims.phi >= 2*pi:
            raise ValueError("Invalid dimensions: phi >= 2*pi")
        
    
    def update_sections(self):
        def sign(x):
            return x / abs(x)
        
        alpha = self.phi/2
        beta  = abs(pi - self.phi)
        theta = pi * (self.phi < pi)
        a = self.r * cos(alpha) / sin(alpha)
        b = self.r * cos(alpha)**2 / sin(alpha) * sign(a)
        c = self.r * cos(alpha)
        d = self.r / sin(alpha) * sign(a)
                
        triangle = self.sections[0]
        triangle[:] = [
            (0,  0),
            (b,  c),
            (b, -c)]
        
        segment = self.sections[1]
        segment.set_dimensions(r=self.r, phi=beta)
        segment.set_position(d1=d, d2=0, theta=theta)
        
        if self.phi > pi:
            self.densities = [-d for d in self.__class__.densities]
        else:
            self.densities = self.__class__.densities[:]
        self.set_density(self.density)
        
        
        
