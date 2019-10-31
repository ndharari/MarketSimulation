import random
from statistics import mean

from collections import deque


class Buyer():
    """
    id = name
    minR = minimum posible reserve price
    maxR = maximum possible reserve price
    alpha = rate of price ajustment
    endurance = max number of failures


    Each Buyer has a different reserve price wich is invariant. Their expected
    prices for each round gets updated following the .expect rule.

    If for the last e pairings the buyer could not buy, it gives up and
    leaves the market. 
    """

    def __init__(self, id, minR, maxR):
        self.__id = id
        self.__name = "B_" + str(id)
        self.__reservePrice = random.randint(minR, maxR)
        self.__expectedPrice = random.randint(minR, self.__reservePrice)
        self.__priceRecord = [self.__expectedPrice]
        self.__paired = False
        self.__traded = False
        self.__alpha = 0.05
        self.__endurance = 3 # Max number of failures it endures
        self.__attrition = deque([0 for i in range(self.__endurance)], 
                                    maxlen = self.__endurance) #list with default lenght
        self.__tired = False

    def getName(self):
        return self.__name

    def getReservePrice(self):
        return self.__reservePrice

    def getExpPrice(self):
        return self.__expectedPrice

    def getPriceRecord(self):
        return self.__priceRecord
    
    def getAttrition(self):
        return self.__attrition

    def getMeanAttrition(self):
        return mean(self.__attrition)

    def updateTraded(self, value):
        self.__traded = value

    def updatePaired(self, value):
        self.__paired = value

    def updateTired(self):
        self.__tired = True

    def resetStates(self):
        self.__traded = False
        self.__paired = False

    def updatePriceRecord(self):
        if self.__tired:
            self.__priceRecord.append(None)
        else:
            self.__priceRecord.append(self.__expectedPrice)

    def updateAttrition(self):
        if self.__paired:
            if self.__traded:
                self.__attrition.append(0)
            else:
                self.__attrition.append(1)

    def expect(self):
        """
        If the Buyer made a deal, he perceives it as thou he can lower his bid.
        If the Buyer doesn't make a deal, he raises its price. The highest possible
        price is the Reserve Price.
        """

        if self.__traded:
            self.__expectedPrice = round(self.__priceRecord[-1] * (1 - self.__alpha) )
        else:
            self.__expectedPrice = min(round(self.__priceRecord[-1]*(1 + self.__alpha) ),
                                             self.__reservePrice)
