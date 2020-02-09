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

import pandas as pd
from collections import OrderedDict

priceList = [i for i in range(5)]
URes = 4
paired = [i^2 for i in range (5)]
traded = [i+5 for i in range (5)]


# o_dict = OrderedDict()
# for i in range (4):
#     o_dict.update(
#         OrderedDict(
#         {sim_id + name + "Precio": priceList,
#         sim_id + name + "Utilidad Reserva": URes,
#         sim_id + name + "Paired": paired,
#         sim_id + name + "Traded": traded
#     }
#     )
#     )


# o_dict


pd.DataFrame.from_dict(o_dict)

from collections import deque
from statistics import mean
dq = deque([0 for i in range(3)], maxlen=3)
dq
dq.append(1)
mean(dq)

a = False
b = True

a and not b

agentlist = []
if not agentlist:
    print("empty")


a = list(range(5))
for b in reversed(a):
    if b == 2:
        a.remove(b)
a

def te_juro(l):
    for b in reversed(l):
        if b==2:
            l.remove(b)

l = [i for i in range (5)]
te_juro(l)
l

a = [1]
b = [1]
c = 5
d = 5
if (a) and (b) and (c <= d):
    print(False)
else:
    print(True)     


if a:
    print("la reputa")