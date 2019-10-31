import random

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class Market():
    """
    Se crea un mercado con lista de compradores y vendedores
    predefinidas. Cada inicio de ronda, los vendedores se mezclan
    y van a acercarse al vendedor que se encuentre más cercano.
    """

    def __init__(self, listSellers, listBuyers, maxrounds=50):
        self.__staticListSellers, self.__staticListBuyers  = listSellers, listBuyers
        self.__dinamicListSellers = list(listSellers) #Needs list() to create the double
        self.__dinamicListBuyers = list(listBuyers) #Needs list() to create the double
        self.__time = 0
        self.__endOfTime = False
        self.__maxrounds = maxrounds

    def moveTime(self):
        if self.__endOfTime:
            print("Cannot, end of times")
        else:
            print("-- \n")
            self.openMarket()
            self.__time += 1

    def exchangeMechanism(self, pair):
        """
        Para aquellos que fueron juntados, se evalúa si se realiza la compra
        Los que evaluan la compra son los compradores. Si el precio ofrecido
        por el vendedor es menor que el precio esperado por el comprador,
        ocurre el intercambio.
        La función toma como input un par de agentes ordenados:
        pair = [seller, buyer]
        Solo afecta el valor de .traded de los agentes
        """
        # Sets local variable names
        seller = pair[0]
        buyer = pair[1]
        # Update paired status
        seller.updatePaired(True)
        buyer.updatePaired(True)
        # Exchange mechanism:
        if seller.getExpPrice() <= buyer.getExpPrice():
            # Prints traded prices.
            print(str(seller.getName()) + " and " +
                    str(buyer.getName()) + " exchange at price " +
                    str(seller.getExpPrice()) + "\n")
            # Updates traded status as True
            seller.updateTraded(True)
            buyer.updateTraded(True)
        else:
            # Prints trade failure
            print(str(seller.getName()) + " and " +
                    str(buyer.getName()) + " did not exchange. \n")
            # Updates traded status as False
            seller.updateTraded(False)
            buyer.updateTraded(False)

    def randomPairing(self, listSellers, listBuyers):
        """
        Gets both the list of sellers and buyers and returns a random paired
        list  always in the shape [[s,b], ...,  [s,b]]
        """
        # Obtiene el largo de las listas
        numSellers = len(listSellers)
        numBuyers = len(listBuyers)

        # Desordena tanto a los compradores como a los vendedores
        listSellers = random.sample(listSellers, numSellers)  # Shuffles Sellers
        listBuyers = random.sample(listBuyers, numBuyers)  # Shuffles Buyers

        # Aparea a los que se juntan
        # Zipea con compradores primero si son más que los vendedores
        if numBuyers >= numSellers:
            return list(zip(listSellers, listBuyers))
        else:
            paired = list(zip(listBuyers, listSellers))  # in reverse!
            return [(s, b) for b, s in paired]

    def dinamicUpdater(self, agentList):
        """
        All agents that are participating in the market reevaluate their preferences
        And update their price records. Cheks if peak attrition has been reached, 
        and drops the laggers from the market. 
        """
        
        for agent in agentList:
            # After the trade, both parts reexamin their preferences.
            agent.expect()
            #And updates their price record
            agent.updatePriceRecord()
            #Updates the dinamic lists
            agent.updateAttrition()
            # If peak endurance reached, remove from list
            if agent.getMeanAttrition() == 1:
                agent.updateTired()
                agentList.remove(agent)
            else:
                agent.resetStates() # And prepares next round
                 
    def openMarket(self):
        """
        Main function of the Market object. When the market opens, Sellers and
        Buyers get paired. Then, the exchange mechanism takes place. After that, all
        agents reevaluate their expectations based considering if the trade did happen,
        regardless if they were paired. Then, sellers and buyers both reset their booleans
        for traded and paired to False. Finally, the market checks if the final round has 
        been reached.
        """
        # Aparea a los que se juntan
        paired = self.randomPairing(self.__dinamicListSellers, 
                                    self.__dinamicListBuyers)

        # Printea los pares
        print("The Buyers and Sellers paired for time " +
              str(self.__time) + " are ")
        print([(s.getName(), b.getName()) for s, b in paired])
        print("\n With expected prices")
        print([(s.getExpPrice(), b.getExpPrice()) for s, b in paired])

        # Ocurre el mecanismo de mercado
        for pair in paired:
            self.exchangeMechanism(pair) #Only affects .traded

        # Makes the agent expect, updates their attrition, their prices and
        # decides who is tired and deletes them
        self.dinamicUpdater(self.__dinamicListSellers)
        self.dinamicUpdater(self.__dinamicListBuyers)

        self.__endOfTime = self.checkEndOfTime()

    def checkEndOfTime(self):
        #Checks also for positive amounts of both buyers and sellers
        if self.__time < self.__maxrounds:
            return False
        return True

    def plotPath(self, agentList, color, alpha):
        for agent in agentList:
            path = agent.getPriceRecord()
            tline = [i for i in range(len(path))]
            plt.plot(tline, path, color, alpha=alpha)

    def graph(self):
        """" 
        Graphs the price path, the costs and the reserve price for all
        sellers and buyers.
        """
        tmax = self.__maxrounds
        t_list = list(range(tmax))

        # Prints the record of expected prices on each round:
        self.plotPath(self.__staticListSellers, '-go', alpha=0.5)
        self.plotPath(self.__staticListBuyers, '-ro', alpha=0.5)

        #Prints bounds
        for s in self.__staticListSellers:
            sellerCost = [s.getCost() for i in range(tmax)]
            plt.plot(t_list, sellerCost, '-g', alpha= 0.2)
        
        for b in self.__staticListBuyers:
            buyerEPrice = [b.getReservePrice() for i in range(tmax)]
            plt.plot(t_list, buyerEPrice, '-r', alpha=0.2)

        # Aestetics
        plt.xlabel("time")
        plt.ylabel("Expected Prices")
        plt.title("Price convergence")
        # Creates the legend with labeling
        seller = mpatches.Patch(color='g', label='Sellers')
        buyer = mpatches.Patch(color='r', label='Buyers')
        plt.legend(handles=[seller, buyer])
        # Plots
        plt.show()

    def getStatic(self, tipe):
        if tipe == "b":
            return len(self.__staticListBuyers)
        else:
            return len(self.__staticListSellers)
        
    def getDinamic(self, tipe):
        if tipe == "b":
            return len(self.__dinamicListBuyers)
        else:
            return len(self.__dinamicListSellers)


            
