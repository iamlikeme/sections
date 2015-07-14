

class Dimensions(object):

    def __init__(self, **kwargs):
        
        object.__setattr__(self, "_Dimensions__dimensions", [])
        
        for key, value in kwargs.items():
            self.__dimensions.append(key)
            setattr(self, key, value)
    

    def __setattr__(self, name, value):
        if name not in self.__dimensions:
            raise AttributeError("Cannot set attribute %s" %name)
        elif isinstance(value, int):
            value = float(value)
        elif isinstance(value, (float, type(None))):
            pass
        else:
            raise TypeError("Cannot set dimension to value of type %s" %type(value))
        
        object.__setattr__(self, name, value)
    

    def __getattribute__(self, name):
        value = object.__getattribute__(self, name)
        
        if name.startswith("_Dimensions"):
            return value
        elif name in self.__dimensions and value is None:
            raise ValueError("Dimension '%s' is not set" %name)
        else:
            return value
