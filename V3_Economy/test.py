class Parent:
    def __init__(self, x, y, VALUE1=1):
        self.__x, self.__y = x, y
        self.__z = None
        self.__value1 = VALUE1

    def get_x(self):
        return self.__x 
    
    def get_y(self):
        return self.__y
    
    def get_z(self):
        return self.__z

    def get_VALUE(self):
        return self.__value1

    def set_z(self, z):
        self.__z = z

class Child0(Parent):
    def __init__(self, x, y, z):
        super().__init__(x, y)
        super().set_z(z + 0)


class Child1(Parent):
    def __init__(self, x, y, z):
        super().__init__(x, y)
        super().set_z(z + 1)


class Child2(Parent):
    def __init__(self, x, y, z):
        super().__init__(x, y)
        super().set_z(z + 2)


cero = Child0(1, 2, 3)

uno = Child1(1, 2, 3)

dos = Child2(1, 2, 3)

dos.get_VALUE()
cero.get_VALUE()
uno.get_VALUE()




