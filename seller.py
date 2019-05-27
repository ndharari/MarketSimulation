import random


class Seller():
    """docstring for Seller"""

    def __init__(self, name, minR, maxR):
        self.__name = name
        self.__traded = False
        self.__reservePrice = random.randint(minR, maxR)
        self.__expectedPrice = random.randint(self.__reservePrice, maxR)
        self.__lastPrice = self.__expectedPrice

    def getName(self):
        return self.__name

    def getReservePrice(self):
        return self.__reservePrice

    def getExpPrice(self):
        return self.__expectedPrice

    def updatePrice(self, price):
        self.__lastPrice = price

    def updateTraded(self, value):
        self.__traded = value

    def expect(self):
        if self.__traded:
            self.__expectedPrice = self.__lastPrice
        elif self.__lastPrice < self.__reservePrice:
            self.__reservePrice
        else:
            self.__expectedPrice = round((self.__lastPrice +
                                          self.__expectedPrice)/2, 2)
