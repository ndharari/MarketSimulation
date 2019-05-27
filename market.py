import random


class Market():
    """Se crea un mercado con lista de compradores y vendedores
    predefinidas. La condición de cierre del mercado es que todos los precios
    por los que se intercambia en t sean iguales a los de t+1.
    Cada inicio de ronda, los vendedores se mezclan y van a acercarse al
    vendedor que se encuentre más cercano"""

    def __init__(self, listSellers, listBuyers, maxrounds=10):
        self.__listBuyers = listBuyers
        self.__listSellers = listSellers
        self.__time = 0
        self.__endOfTime = False
        self.__maxrounds = maxrounds
        # self.__thisRound = []
        # self.__record = []

    def moveTime(self):
        if self.__endOfTime:
            print("Cannot, end of times")
        else:
            print("-- \n")
            self.openMarket()
            self.__time += 1

    def openMarket(self):
        # Los vendedores están quietos en su lugar. Los compradores
        # van al vendedor ubicado en su mismo lugar en la lista de
        # vendedores

        random.shuffle(self.__listBuyers)  # Shuffles Buyers
        paired = list(zip(self.__listSellers, self.__listBuyers))
        print("The Buyers and Sellers paired for time " +
              str(self.__time) + " are ")
        print([(x.getName(), y.getName()) for x, y in paired])
        print("\n With expected prices ")
        print([(x.getExpPrice(), y.getExpPrice()) for x, y in paired])

        # Los que evaluan la compra son los compradores. Si el precio ofrecido
        # cierra, compran. Luego, ambos reevaluan sus precios.
        for pair in paired:
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

        # self.__record.append()
        self.__endOfTime = self.checkEndOfTime()

    # def updateRecord(self):
    #    None

    def checkEndOfTime(self):
        if self.__time < self.__maxrounds:
            return False
        return True

    def ended(self):
        return self.__endOfTime
