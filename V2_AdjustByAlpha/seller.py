import random


class Seller():
    """
    id = name
    minC = minimum posible cost
    maxC = max possible cost

    Each Seller has a different cost wich is invariant. Their expected
    prices for each round gets updated following the .expect rule
    """

    def __init__(self, id, minC, maxC):
        self.__id = id
        self.__name = "S_" + str(id)
        self.__cost = random.randint(minC, maxC)
        self.__expectedPrice = random.randint(self.__cost, maxC)
        self.__record = [self.__expectedPrice]
        self.__paired = False
        self.__traded = False
        self.__alpha = 0.05

    def getName(self):
        return self.__name

    def getExpPrice(self):
        return self.__expectedPrice

    def getRecord(self):
        return self.__record

    def getCost(self):
        return self.__cost

    def updateTraded(self, value):
        self.__traded = value

    def updatePaired(self, value):
        self.__paired = value

    def reseteStates(self):
        self.__traded = False
        self.__paired = False
    
    def record(self):
        self.__record.append(self.__expectedPrice)

    def expect(self):
        """
        If the Seller made a deal, he perceives it as thou he could raice prices.
        If the Seller doesn't make a deal, he lowers its price. The lowest possible
        price is the cost.
        """
        if self.__traded:
            self.__expectedPrice = round(self.__record[-1] * (1 + self.__alpha), 2)
        else:
            self.__expectedPrice = max(round(self.__record[-1]*(1 - self.__alpha), 2),
                                             self.__cost)


