import random
import matplotlib.pyplot as plt

class Market():
    """Se crea un mercado con lista de compradores y vendedores
    predefinidas. La condición de cierre del mercado es que todos los precios
    por los que se intercambia en t sean iguales a los de t+1.
    Cada inicio de ronda, los vendedores se mezclan y van a acercarse al
    vendedor que se encuentre más cercano"""

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

    def openMarket(self):

        numSellers = len(self.__listSellers)
        numBuyers = len(self.__listBuyers)

        # Desordena tanto a los compradores como a los vendedores
        Shuf_Sellers = random.sample(self.__listSellers, numSellers) # Shuffles Sellers
        Shuf_Buyers = random.sample(self.__listBuyers, numBuyers) # Shuffles Buyers

        # Aparea a los que se juntan
        # zipea con compradores primero si son más que los vendedores
        if numBuyers >= numSellers:
            paired = list(zip(Shuf_Sellers, Shuf_Buyers))  
        else:
            paired = list(zip(Shuf_Buyers, Shuf_Sellers)) #in reverse!
            paired = [(s, b) for s, b in paired]
        
        # Aparea a los que se juntan
        print("The Buyers and Sellers paired for time " +
              str(self.__time) + " are ")
        print([(x.getName(), y.getName()) for x, y in paired])
        print("\n With expected prices ")
        print([(x.getExpPrice(), y.getExpPrice()) for x, y in paired])

        # Para aquellos que fueron juntados, se evalúa si se realiza la compra
        # Los que evaluan la compra son los compradores. Si el precio ofrecido
        # cierra, compran. Luego, ambos reevaluan sus precios.
        for pair in paired:
            pair[0].updatePaired(True)
            pair[1].updatePaired(True)
            if pair[0].getExpPrice() <= pair[1].getExpPrice():
                print(str(pair[0].getName()) + " and " +
                      str(pair[1].getName()) + " exchange at price " +
                      str(pair[0].getExpPrice()) + "\n")
                pair[0].updateTraded(True)
                pair[1].updateTraded(True)
            else:
                print(str(pair[0].getName()) + " and " +
                      str(pair[1].getName()) + " did not exchange. \n")
                pair[0].updateTraded(False)
                pair[1].updateTraded(False)

            # Buyer sets Last price as the expected from costumer.
            pair[0].updatePrice(pair[1].getExpPrice())
            pair[1].updatePrice(pair[0].getExpPrice())
            # Prepares next round
            pair[0].expect()
            pair[1].expect()

        # Records time and prices for both sellers and buyers
        for seller in self.__listSellers:
            seller.record(self.__time)
        for buyer in self.__listBuyers:
            buyer.record(self.__time)
        
        self.__endOfTime = self.checkEndOfTime()

    def checkEndOfTime(self):
        if self.__time < self.__maxrounds:
            return False
        return True

    def ended(self):
        return self.__endOfTime

    def graph(self):
        # Graphs the convcergence
        plt.xlabel("time")
        plt.ylabel("Expected Prices")
        plt.title("Price convergence")
        for t in range(self.__maxrounds):
            for b in self.__listBuyers:
                l = b.getRecord()
                plt.plot(t, l[t][1], 'r.')
            for s in self.__listSellers:
                l = s.getRecord()
                plt.plot(t, l[t][1], 'g.')
        plt.legend()
        plt.show()
