from operator import attrgetter
from math import sin, cos

class cached_property(object):
    """ A property that is only computed once per instance and then replaces
        itself with an ordinary attribute. Deleting the attribute resets the
        property.

        Source: https://github.com/bottlepy/bottle/commit/fa7733e075da0d790d809aa3d2f53071897e6f76
        """
    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value



class Dimensions(object):

    def __init__(self, **kwargs):
        
        object.__setattr__(self, "_Dimensions__dimensions", [])
        
        for key, value in kwargs.items():
            self.__dimensions.append(key)
            setattr(self, key, value)
    
    
    def update(self, **kwargs):
        for name, value in kwargs.items():
            self.__convert_dimension(value)
            if name not in self.__dimensions:
                setattr(self, name, value)
        for name, value in kwargs.items():
            setattr(self, name, value)
    
    
    def to_dict(self):
        return {name:object.__getattribute__(self, name) for name in self.__dimensions}
    

    def copy(self):
        return Dimensions(**self.to_dict())
    
    
    def __convert_dimension(self, value):
        if isinstance(value, int):
            value = float(value)
        elif isinstance(value, (float, type(None))):
            pass
        else:
            raise TypeError("Cannot set dimension to value of type %s" %type(value))
        return value
    

    def __setattr__(self, name, value):
        if name not in self.__dimensions:
            raise AttributeError("Cannot set attribute %s" %name)
        
        value = self.__convert_dimension(value)
        object.__setattr__(self, name, value)
    

    def __getattribute__(self, name):
        value = object.__getattribute__(self, name)
        
        if name.startswith("_Dimensions"):
            return value
        elif name in self.__dimensions and value is None:
            raise ValueError("Dimension '%s' is not set" %name)
        else:
            return value
    

    def __repr__(self):
        return "Dimensions%s" %self.to_dict()
        


class VertexArray(object):
    
    def __init__(self, n=0):
        self.__vertices = []
        self.n = n
    
    
    def copy(self):
        va = self.__class__(self.n)
        va[:] = self[:]
        return va
        
    
    @property
    def n(self):
        return len(self)
    
    
    @n.setter
    def n(self, value):
        if isinstance(value, int):
            delta = value - self.n
        else:
            raise TypeError("n must be an int, got %s" %value)
        
        if delta >= 0:
            self.__vertices += [None] * delta
        else:
            self.__vertices = self.__vertices[:value]
    
    
    def __convert_to_vertex(self, value):
        try:
            x, y = value
        except ValueError:
            raise TypeError("Cannot set vertex to %r" %value)
        
        if type(x) not in (float, int) or type(y) not in (float, int):
            raise TypeError("Vertex coordinates must be two numbers, got %r and %r" %(x,y))
        
        return float(x), float(y)
        
    
    def __len__(self):
        return len(self.__vertices)
    
    
    def __getitem__(self, index):
        vertex = self.__vertices[index]
        if vertex is None:
            raise ValueError("Vertex %i is not set" %index)
        return vertex
    
    
    def __setitem__(self, index, value):
        self.__vertices[index]  # Check if index is within range
        if value is not None:
            value = self.__convert_to_vertex(value)
        self.__vertices[index] = value
    
    
    def __setslice__(self, i, j, value):
        vertices = self.__vertices[:]
        vertices.__setslice__(i, j, value)
        vertices = [self.__convert_to_vertex(v) for v in vertices]
        if len(vertices) != self.n:
            raise ValueError("It is not allowed to change the number of vertices by slicing")
        else:
            self.__vertices = vertices
    
    
    def __repr__(self):
        return "VertexArray%s" %repr(self.__vertices)


class SectionType(type):
    
    def __init__(cls, *args, **kwargs):
        for name in cls.dimensions.to_dict():
            setattr(cls, name, property(attrgetter("dimensions.%s" %name)))


class BaseSection(object):
    __metaclass__ = SectionType
    dimensions = Dimensions()
    
    def __init__(self, **kwargs):
        self.__density  = None
        self.__position = (0.0, 0.0, 0.0)
        self.dimensions = self.__class__.dimensions.copy()
        
        self.set_density(kwargs.pop("density", 1.0))
        
        dimensions = self.dimensions.to_dict()
        dimensions.update(kwargs)
        fully_defined = all(dim is not None for dim in dimensions.values())
        
        if fully_defined:        
            self.set_dimensions(**dimensions)
        else:
            self.dimensions.update(**dimensions)


    # Setters and getters for attributes that affect the physical
    # properties of the section: density, dimensions, position
    # ===========================================================        
    
    @property
    def density(self):
        return self.__density
    
    
    @property
    def position(self):
        return self.__position
    
    
    def set_density(self, value):
        value = float(value)
        if value:
            self.__density = float(value)
        else:
            raise ValueError("Cannot set density to zero")
    

    def set_dimensions(self, **kwargs):
        dims = self.dimensions.copy()
        dims.update(**kwargs)
        self.check_dimensions(dims)
        
        self.dimensions.update(**kwargs)
    
    
    def set_position(self, d1=None, d2=None, theta=None):
        position = list(self.__position)
        if d1 is not None:
            position[0] = float(d1)
        if d2 is not None:
            position[1] = float(d2)
        if theta is not None:
            position[2] = float(theta)
        self.__position = tuple(position)

    # ===========================================================
    
    def check_dimensions(self, dims):
        """
        This function is called by set_dimensions before section dimensions
        are updated. The function should raise a ValueError if *dims* (a Dimensions
        object) is an invalid combination of dimensions."""
        pass
        
    
    def transform_to_global(self, vector_or_matrix):
        x0, y0, theta = self.position
        s = sin(theta)
        c = cos(theta)
        
        data = tuple(vector_or_matrix)
        if len(data) == 2:
            x, y = [float(v) for v in data]
            x_ = x0 + x*c - y*s
            y_ = y0 + x*s + y*c
            return x_, y_
        elif len(data) == 3:
            xx, yy, xy = [float(v) for v in data]
            xx_ = c*c * xx - 2*s*c * xy + s*s * yy
            yy_ = s*s * xx + 2*s*c * xy + c*c * yy
            xy_ = (c*c - s*s) * xy + s*c * (xx - yy)
            return xx_, yy_, xy_
        else:
            raise TypeError("vector_or_matrix must be a sequence of 2 or 3 elements, got %s" %repr(vector_or_matrix))


    def parallel_axis(self, I, cog, reverse=False):
        A = self.A
        _I11, _I22, _I12 = I
        e1, e2 = cog
        if reverse:
            f = -1.0
        else:
            f = 1.0
        I11 = _I11 + f*A*e2*e2
        I22 = _I22 + f*A*e1*e1
        I12 = _I12 + f*A*e1*e2
        return I11, I22, I12


    # Physical properties of the section
    # ==================================
    
    # Naming conventions for physical properties:
    # * names starting with undescore refer to properties in the local csys
    # * names ending with zero refer to properties in a csys translated to the cog

    # Physical properties to be implemented in a subclass
    # ---------------------------------------------------
    
    @property
    def _cog(self):
        """
        Position of the centre of gravity in the local csys."""
        raise NotImplementedError
    

    @property
    def A(self):
        """
        Surface area (mass)"""
        raise NotImplementedError
    
    
    @property
    def _I0(self):
        """
        Moments of inertia (I11, I22, I12) in the local csys translated to the cog."""
        raise NotImplementedError
    
    
    # Other physical properties
    # ---------------------------------------------------
    
    @property
    def cog(self):
        """
        Position of the centre of gravity in the global csys."""
        return self.transform_to_global(self._cog)

    
    @property
    def I0(self):
        """
        Moment of inertia (I11, I22, I12) in the global csys translated to the cog."""
        return self.transform_to_global(self._I0)
    
    
    @property
    def _I(self):
        """
        Moments of inertia (I11, I22, I12) in the local csys."""
        return self.parallel_axis(self._I0, self._cog)
    
    
    @property
    def I(self):
        """
        Moments of inertia (I11, I22, I12) in the global csys."""
        return self.parallel_axis(self.I0, self.cog)


class SimpleSection(BaseSection):
    pass


class ComplexSection(BaseSection):
    
    sections  = NotImplemented
    densities = NotImplemented

    def update_sections(self):
        raise NotImplementedError


    def __init__(self, **kwargs):
        self.sections = [cls() for cls in self.__class__.sections]
    
        if self.densities is NotImplemented:
            self.densities = [1.0 for s in self.sections]
        else:
            self.densities = [float(d) for d in self.densities]
        
        if len(self.densities) != len(self.sections):
            raise ValueError("The numbers of sections and densities do not match")
        
        super(ComplexSection, self).__init__(**kwargs)
    
    
    def set_density(self, value):
        super(ComplexSection, self).set_density(value)
        for section, density in zip(self.sections, self.densities):
            section.set_density(value*density)
            

    def set_dimensions(self, **kwargs):
        super(ComplexSection, self).set_dimensions(**kwargs)
        self.update_sections()
    
    
    # Physical properties to be implemented in a subclass
    # ---------------------------------------------------
    @property
    def _cog(self):
        """
        Position of the centre of gravity in the local csys."""
        S1 = sum(section.A * section.cog[1] for section in self.sections)
        S2 = sum(section.A * section.cog[0] for section in self.sections)
        _e1 = S2 / self.A
        _e2 = S1 / self.A
        return _e1, _e2
    

    @property
    def A(self):
        """
        Surface area (mass)"""
        return sum(section.A for section in self.sections)
    
    
    @property
    def _I0(self):
        """
        Moments of inertia (I11, I22, I12) in the local csys translated to the cog."""
        I11 = sum(section.I[0] for section in self.sections)
        I22 = sum(section.I[1] for section in self.sections)
        I12 = sum(section.I[2] for section in self.sections)
        return self.parallel_axis((I11, I22, I12), self._cog, reverse=True)
        
        
        

