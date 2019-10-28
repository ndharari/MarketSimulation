import random


class Buyer():
    """docstring for Buyer"""

    def __init__(self, id, minR, maxR):
        self.__id = id
        self.__name = "B_" + str(id)
        self.__traded = False
        self.__reservePrice = random.randint(minR, maxR)
        self.__expectedPrice = random.randint(minR, self.__reservePrice)
        self.__record = [self.__expectedPrice]
        self.__paired = False
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

    def prepareNext(self):
        self.__traded = False
        self.__paired = False

    def expect(self):
        if self.__traded:
            self.__expectedPrice = round(self.__record[-1]*(1+self.__alpha), 2)
        else:
            self.__expectedPrice = min(round(self.__record[-1]*(1-self.__alpha), 2),
                                             self.__reservePrice)

    def record(self, time):
        self.__record.append(self.__expectedPrice)
