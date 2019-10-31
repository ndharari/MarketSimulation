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
        self.__staticListBuyers, self.__dinamicListBuyers  = listBuyers, listBuyers
        self.__staticListSellers, self.__dinamicListSellers = listSellers, listSellers
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
        ocurre el intercambio. Luego, ambos reevaluan sus expectativas.
        La función toma como input un par de agentes ordenados:
        pair = [seller, buyer]
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
            # Updates traded status as True
            seller.updateTraded(False)
            buyer.updateTraded(False)
        # After the trade, both parts reexamin their preferences.
        seller.expect()
        buyer.expect()

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

    def dinamicUpdater(self, dinamicAgentList):
        """
        Cheks if peak attrition has been reached, and drops the laggers
        from the market. 
        """
        #Updates the dinamic lists
        for agent in dinamicAgentList:
            agent.updateAttrition()
            # If peak andurance reached, remove from list
            if agent.getMeanAttrition() == 1:
                agent.updateTired()
                dinamicAgentList.remove(agent)
            else:
                agent.resetStates() # And prepares next round
                 
    def openMarket(self):
        """
        Main function of the Market object. When the market opens, Sellers and
        Buyers get paired. Then, the exchange mechanism takes place. Then,
        sellers and buyers both reset their booleans for traded and paired to False.
        Finally, the market checks if the final round has been reached.
        """

        # Aparea a los que se juntan
        paired = self.randomPairing(self.__dinamicListSellers, 
                                    self.__dinamicListBuyers)

        # Printea los pares
        print("The Buyers and Sellers paired for time " +
              str(self.__time) + " are ")
        print([(s.getName(), b.getName()) for s, b in paired])
        print("\n With cost and expected price ")
        print([(s.getCost(), b.getExpPrice()) for s, b in paired])

        # Ocurre el mecanismo de mercado
        for pair in paired:
            self.exchangeMechanism(pair)

        # Dinamic lists drop the laggers
        self.dinamicUpdater(self.__dinamicListSellers)
        self.dinamicUpdater(self.__dinamicListBuyers)

        for s in self.__staticListSellers:
            s.updatePriceRecord()
        
        for b in self.__staticListBuyers:
            b.updatePriceRecord()

        self.__endOfTime = self.checkEndOfTime()

    def checkEndOfTime(self):
        if self.__time < self.__maxrounds:
            return False
        return True

    def graph(self):
        """" 
        Graphs the price path, the costs and the reserve price for all
        sellers and buyers.
        """
        tmax = self.__maxrounds + 1
        plt.xlabel("time")
        plt.ylabel("Expected Prices")
        plt.title("Price convergence")
        t_list = list(range(tmax))

        # Graphs the record of expected prices on each round
        # and all-time costs for all Sellers
        for s in self.__staticListSellers:
            #Plots the price record for the endured turns
            sellerRec = s.getPriceRecord()
            plt.plot(t_list, sellerRec, '-go', alpha=0.5)
            
            #Plots the cost for all t
            sellerCost = [s.getCost() for i in range(tmax)]
            plt.plot(t_list, sellerCost, '-g', alpha= 0.2)

        # Graphs the record of expected prices on each round
        # and all-time Expected Prices for all Buyers
        for b in self.__staticListBuyers:
            #Plots the price record for the endured turns
            buyerRec = b.getPriceRecord()
            plt.plot(t_list, buyerRec, '-ro', alpha=0.5)
            
            #Plots the reserve price for all t
            buyerEPrice = [b.getReservePrice() for i in range(tmax)]
            plt.plot(t_list, buyerEPrice, '-r', alpha= 0.2)
        
        # Creates the legend with labeling
        seller = mpatches.Patch(color ='g', label='Sellers')
        buyer = mpatches.Patch(color ='r', label='Buyers')
        plt.legend(handles=[seller, buyer])

        # Plots
        plt.show()
