import random

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class Market():
    """
    Se crea un mercado con lista de compradores y vendedores
    predefinidas. La condición de cierre del mercado es que todos los precios
    por los que se intercambia en t sean iguales a los de t+1.
    Cada inicio de ronda, los vendedores se mezclan y van a acercarse al
    vendedor que se encuentre más cercano
    """

    def __init__(self, listSellers, listBuyers, maxrounds=50):
        self.__listBuyers = listBuyers
        self.__listSellers = listSellers
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
        #Sets local variable names 
        seller = pair[0]
        buyer = pair[1]
        #Update paired status
        seller.updatePaired(True)
        buyer.updatePaired(True)
        #Exchange mechanism:
        if seller.getExpPrice() <= buyer.getExpPrice():
            #Prints traded prices.
            print(str(seller.getName()) + " and " +
                    str(buyer.getName()) + " exchange at price " +
                    str(seller.getExpPrice()) + "\n")
            #Updates traded status as True
            seller.updateTraded(True)
            buyer.updateTraded(True)
        else:
            #Prints trade failure
            print(str(seller.getName()) + " and " +
                    str(buyer.getName()) + " did not exchange. \n")
            #Updates traded status as True
            seller.updateTraded(False)
            buyer.updateTraded(False)
        # Prepares next round CHECK IF NEEDED
        seller.expect()
        buyer.expect()
    
    def randomPairing(self, listSellers, listBuyers):
        """
        Gets both the list of sellers and buyers and returns a random paired
        list  always in the shape [[s,b], ...,  [s,b]]
        """
        #Obtiene el largo de las listas
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

    def openMarket(self):
        """
        Main function of the Market object. When the market opens, Sellers and
        Buyers get paired. Then, the exchange mechanism takes place. Then, 
        sellers and buyers both reset their booleans for traded and paired to False.
        Finally, the market checks if the final round has been reached.
        """

        # Aparea a los que se juntan
        paired = self.randomPairing(self.__listSellers, self.__listBuyers)

        # Printea los pares
        print("The Buyers and Sellers paired for time " +
              str(self.__time) + " are ")
        print([(s.getName(), b.getName()) for s, b in paired])
        print("\n With cost and expected price ")
        print([(s.getCost(), b.getExpPrice()) for s, b in paired])

        # Ocurre el mecanismo de mercado
        for pair in paired:
            self.exchangeMechanism(pair)

        # Records time and prices for both sellers and buyers
        # And prepares next round
        for seller in self.__listSellers:
            seller.record()
            seller.reseteStates()
        for buyer in self.__listBuyers:
            buyer.record()
            buyer.reseteStates()

        self.__endOfTime = self.checkEndOfTime()

    def checkEndOfTime(self):
        if self.__time < self.__maxrounds:
            return False
        return True

    def graph(self):
        # Graphs the convcergence
        plt.xlabel("time")
        plt.ylabel("Expected Prices")
        plt.title("Price convergence")
        t_list = list(range(self.__maxrounds + 1))

        #Graphs the record of expected prices in each round for Sellers
        for s in self.__listSellers:
            sellerRec = s.getRecord()
            plt.plot(t_list, sellerRec, '-go', alpha=0.5)

        #Graphs the record of expected prices in each round for Buyers
        for b in self.__listBuyers:
            buyerRec = b.getRecord()
            plt.plot(t_list, buyerRec, '-ro', alpha=0.5)
        
        #Creates the legend with labeling
        seller = mpatches.Patch(color='g', label='Sellers')
        buyer = mpatches.Patch(color='r', label='Buyers')
        plt.legend(handles=[seller, buyer])

        #Plots
        plt.show()
        



