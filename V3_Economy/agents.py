from statistics import mean
from collections import deque
from random import uniform


class Agent:
    """
    Parent class for agents in the game. Not suposed to be used alone.

    id = name. 
    min = minimum posible cost/reserve price. 
    max = maximum possible reserve price. 
    tipe = "alpha" or "delta". 
    alpha = rate of price ajustment. 
    delta = fixed rate of price ajustment. 
    endurance = max number of failures. 
    r = rounding parameter. 
    """

    def __init__(self, id, min, max, endurance=3, tipe="delta", delta=0.5,
                 alpha=0.05, r=2):
        
        #Sets the parameters
        self.id, self.tipe, self.delta, self.round = id, tipe, delta, r
        self.alpha, self.endurance = alpha, endurance 
        
        self.attrition = deque([0 for i in range(self.endurance)],
                                 maxlen=self.endurance)  # list with default lenght
        
        self.paired = self.traded = self.tired = False
        
        self.name = self.expectedPrice = self.priceRecord = None  # Placeholders

    def getMeanAttrition(self): 
        return mean(self.attrition)

    def updatePriceRecord(self): 
        if self.tired:
            self.priceRecord.append(None)
        else:
            self.priceRecord.append(self.expectedPrice)
    
    def updateAttrition(self): 
        if self.paired:
            if self.traded:
                self.attrition.append(0)
            else:
                self.attrition.append(1)
    
    def resetStates(self): 
        #TODO: DELETE FUNCTION WHEN RECORD IS ADDED
        self.traded = False
        self.paired = False

    # Expect functions, for children. Required by .expect()

    def expectByAlpha(self):
        pass

    def expectByDelta(self):
        pass

    def expect(self):
        """
        Checks which expecting mechanism is used and implements it. 
        Requires tipe = ["alpha", "delta"]
        Alpha -> P(t+1) = (1-alpha) * P(t) if traded
        Delta -> P(t+1) = P(t) - Delta  if traded

        """
        tipe = self.tipe
        if tipe == "delta":
            self.expectByDelta()
        elif tipe == "alpha":
            self.expectByAlpha()
        else:
            raise NameError

    def restart(self):
        """
        Restarts the agent for another simulation of the market
        """
        
        self.expectedPrice = self.priceRecord[0]
        self.priceRecord = [self.expectedPrice]
        self.paired = self.traded = self.tired = False


class Buyer(Agent):
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
        super().__init__(id, minR, maxR, endurance, tipe, delta,
                         alpha, r)

        self.reservePrice = round(uniform(minR, maxR), self.round)
        self.name = "B_" + str(id)
        self.expectedPrice = round(uniform(minR, self.reservePrice), self.round)
        self.priceRecord = [self.expectedPrice]

    def getReservePrice(self):
        return self.reservePrice

    def expectByAlpha(self):
        """
        If the Buyer made a deal, he perceives it as thou he can lower his bid.
        If the Buyer doesn't make a deal, he raises its price. The highest possible
        price is the Reserve Price.
        The general rule applied is:

        P(t+1) = (1-alpha) * P(t) if traded
        """
        r, alpha = self.round, self.alpha
        if self.traded:
            self.expectedPrice = round(
                self.priceRecord[-1] * (1 - alpha), r)
        else:
            self.expectedPrice = min(round(self.priceRecord[-1]*(1 + alpha), r),
                                       self.reservePrice)

    def expectByDelta(self):
        """
        If the Buyer made a deal, he perceives it as thou he can lower his bid.
        If the Buyer doesn't make a deal, he raises its price. The highest possible
        price is the Reserve Price.
        The general rule applied is:

        P(t+1) = P(t) - Delta  if traded
        """

        delta = self.delta
        if self.traded:
            self.expectedPrice = self.priceRecord[-1] - delta
        else:
            self.expectedPrice = min(self.priceRecord[-1] + delta,
                                       self.reservePrice)

class Seller(Agent):
    """
    id = name
    minC = minimum posible cost
    maxC = max possible cost
    tipe = "alpha" or "delta"
    alpha = rate of price ajustment
    delta = fixed rate of price ajustment
    endurance = max number of failures
    r = rounding parameter

    Each Seller has a different cost wich is invariant. Their expected
    prices for each round gets updated following the .expect rule

    If for the last e pairings the seller could not sell, it gives up and
    leaves the market. 
    """

    def __init__(self, id, minC, maxC, endurance=3, tipe="delta", delta=0.5,
                 alpha=0.05, r=2):
        super().__init__(id, minC, maxC, endurance, tipe, delta,
                         alpha, r)

        self.cost = round(uniform(minC, maxC), self.round)
        self.name = "S_" + str(id)
        self.expectedPrice = round(uniform(self.cost, maxC), self.round)
        self.priceRecord = [self.expectedPrice]


    def getCost(self):
        return self.cost

    def expectByAlpha(self):
        """
        If the Seller made a deal, he perceives it as thou he could raice prices.
        If the Seller doesn't make a deal, he lowers its price. The lowest possible
        price is the cost.
        The general rule applied is:

        P(t+1) = (1+alpha) * P(t) if traded
        """
        r, alpha = self.round, self.alpha
        if self.traded:
            self.expectedPrice = round(
                self.priceRecord[-1] * (1 + alpha), r)
        else:
            self.expectedPrice = max(round(self.priceRecord[-1]*(1 - alpha), r),
                                       self.cost)

    def expectByDelta(self):
        """
        If the Seller made a deal, he perceives it as thou he could raice prices.
        If the Seller doesn't make a deal, he lowers its price. The lowest possible
        price is the cost.
        The general rule applied is:

        P(t+1) = Delta + P(t) if traded
        """

        delta = self.delta
        if self.traded:
            self.expectedPrice = self.priceRecord[-1] + delta
        else:
            self.expectedPrice = max(self.priceRecord[-1] - delta,
                                       self.cost)
