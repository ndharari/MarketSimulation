from random import uniform
from statistics import mean
from collections import deque

class Buyer():
    """
    id = name
    minR = minimum posible reserve price
    maxR = maximum possible reserve price
    tipe = "alpha" or "delta"
    alpha = rate of price ajustment
    delta = fixed rate of price ajustment
    endurance = max number of failures
    r = rounding parameter

    Each Buyer has a different reserve price wich is invariant. Their expected
    prices for each round gets updated following the .expect rule.

    If for the last e pairings the buyer could not buy, it gives up and
    leaves the market. 
    """

    def __init__(self, id, minR, maxR, endurance=3, tipe="delta", delta=0.5,
                 alpha=0.05, r=2):
        self.__id = id
        self.__name = "B_" + str(id)
        self.__tipe = tipe
        self.__delta = delta
        self.__round = r
        self.__alpha = alpha
        self.__endurance = endurance  # Max number of failures it endures
        self.__paired = False
        self.__traded = False
        self.__tired = False
        self.__reservePrice = round(uniform(minR, maxR), self.__round)
        self.__expectedPrice = round(uniform(minR, self.__reservePrice), self.__round)
        self.__priceRecord = [self.__expectedPrice]
        self.__attrition = deque([0 for i in range(self.__endurance)], 
                                    maxlen = self.__endurance) # list with default lenght

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
        Checks which expecting mechanism is used and implements it. 
        Requires tipe = ["alpha", "delta"]
        Alpha -> P(t+1) = (1-alpha) * P(t) if traded
        Delta -> P(t+1) = P(t) - Delta  if traded

        """
        tipe = self.__tipe
        if tipe == "delta":
            self.expectByDelta()
        elif tipe == "alpha":
            self.expectByAlpha()
        else:
            raise NameError

    def expectByAlpha(self):
        """
        If the Buyer made a deal, he perceives it as thou he can lower his bid.
        If the Buyer doesn't make a deal, he raises its price. The highest possible
        price is the Reserve Price.
        The general rule applied is:

        P(t+1) = (1-alpha) * P(t) if traded
        """
        r, alpha = self.__round, self.__alpha
        if self.__traded:
            self.__expectedPrice = round(
                self.__priceRecord[-1] * (1 - alpha), r)
        else:
            self.__expectedPrice = min(round(self.__priceRecord[-1]*(1 + alpha), r),
                                       self.__reservePrice)

    def expectByDelta(self):
        """
        If the Buyer made a deal, he perceives it as thou he can lower his bid.
        If the Buyer doesn't make a deal, he raises its price. The highest possible
        price is the Reserve Price.
        The general rule applied is:

        P(t+1) = P(t) - Delta  if traded
        """

        delta = self.__delta
        if self.__traded:
            self.__expectedPrice = self.__priceRecord[-1] - delta
        else:
            self.__expectedPrice = min(self.__priceRecord[-1] + delta, 
                                       self.__reservePrice)
