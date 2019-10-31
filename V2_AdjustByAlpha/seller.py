import random
from statistics import mean

from collections import deque

class Seller():
    """
    id = name
    minC = minimum posible cost
    maxC = max possible cost
    alpha = rate of price ajustment
    endurance = max number of failures

    Each Seller has a different cost wich is invariant. Their expected
    prices for each round gets updated following the .expect rule

    If for the last e pairings the seller could not sell, it gives up and
    leaves the market. 
    """

    def __init__(self, id, minC, maxC):
        self.__id = id
        self.__name = "S_" + str(id)
        self.__cost = random.randint(minC, maxC)
        self.__expectedPrice = random.randint(self.__cost, maxC)
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

    def getExpPrice(self):
        return self.__expectedPrice

    def getPriceRecord(self):
        return self.__priceRecord

    def getCost(self):
        return self.__cost
    
    def getAttrition(self):
        return self.__attrition
    
    def getMeanAttrition(self):
        return mean(self.__attrition)

    def updateTraded(self, value):
        self.__traded = value

    def updatePaired(self, value):
        self.__paired = value

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
            
    def updateTired(self):
        self.__tired = True

    def expect(self):
        """
        If the Seller made a deal, he perceives it as thou he could raice prices.
        If the Seller doesn't make a deal, he lowers its price. The lowest possible
        price is the cost.
        """
        if self.__traded:
            self.__expectedPrice = round(self.__priceRecord[-1] * (1 + self.__alpha) )
        else:
            self.__expectedPrice = max(round(self.__priceRecord[-1]*(1 - self.__alpha) ),
                                             self.__cost)
    
    