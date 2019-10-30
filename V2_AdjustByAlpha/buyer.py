import random


class Buyer():
    """
    id = name
    minR = minimum posible reserve price
    maxR = maximum possible reserve price

    Each Buyer has a different reserve price wich is invariant. Their expected
    prices for each round gets updated following the .expect rule.
    """

    def __init__(self, id, minR, maxR):
        self.__id = id
        self.__name = "B_" + str(id)
        self.__reservePrice = random.randint(minR, maxR)
        self.__expectedPrice = random.randint(minR, self.__reservePrice)
        self.__record = [self.__expectedPrice]
        self.__paired = False
        self.__traded = False
        self.__alpha = 0.05

    def getName(self):
        return self.__name

    def getReservePrice(self):
        return self.__reservePrice

    def getExpPrice(self):
        return self.__expectedPrice

    def getRecord(self):
        return self.__record

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
        If the Buyer made a deal, he perceives it as thou he can lower his bid.
        If the Buyer doesn't make a deal, he raises its price. The highest possible
        price is the Reserve Price.
        """

        if self.__traded:
            self.__expectedPrice = round(self.__record[-1] * (1 - self.__alpha), 2)
        else:
            self.__expectedPrice = min(round(self.__record[-1]*(1 + self.__alpha), 2),
                                             self.__reservePrice)


