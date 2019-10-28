import random


class Seller():
    """docstring for Seller"""

    def __init__(self, id, minR, maxR):
        self.__id = id
        self.__name = "S_" + str(id)
        self.__traded = False
        self.__reservePrice = random.randint(minR, maxR)
        self.__expectedPrice = random.randint(self.__reservePrice, maxR)
        self.__lastPrice = self.__expectedPrice
        self.__record = [self.__expectedPrice]
        self.__paired = False

    def getName(self):
        return self.__name

    def getReservePrice(self):
        return self.__reservePrice

    def getExpPrice(self):
        return self.__expectedPrice

    def getRecord(self):
        return self.__record

    def updatePrice(self, price):
        self.__lastPrice = price

    def updateTraded(self, value):
        self.__traded = value

    def updatePaired(self, value):
        self.__paired = value

    def prepareNext(self):
        self.__traded = False

    def expect(self):
        if self.__traded:
            self.__expectedPrice = self.__lastPrice
        else:
            self.__expectedPrice = max(round((self.__lastPrice +
                                             self.__expectedPrice)/2, 2),
                                       self.__reservePrice)
        self.prepareNext()

    def record(self, time):
        self.__record.append(self.__expectedPrice)