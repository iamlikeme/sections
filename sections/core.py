

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
    
    
    @property
    def n(self):
        return len(self)
    
    
    @n.setter
    def n(self, value):
        if not isinstance(value, int):
            raise TypeError("n must be an int, got %s" %value)
        self.__vertices = [None] * value
    
    
    def __convert_to_vertex(self, value):
        try:
            x, y = value
        except ValueError:
            raise TypeError("Cannot set vertex to '%r'" %value)
        
        if type(x) not in (float, int) or type(y) not in (float, int):
            raise TypeError("Vertex coordinates must be two numbers, got '%r' and '%r'" %(x,y))
        
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
        
    
    def __repr__(self):
        return repr(self.__vertices)
