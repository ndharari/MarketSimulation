import pandas as pd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from random import sample
from collections import OrderedDict

import pandas as pd

import altair as alt
from altair_saver import save

class Market():
    """
    Se crea un mercado con lista de compradores y vendedores
    predefinidas. Cada inicio de ronda, los vendedores se mezclan
    y van a acercarse al vendedor que se encuentre más cercano.
    """

    def __init__(self, listSellers, listBuyers, maxrounds=50, echo=True):
        self.staticListSellers, self.staticListBuyers = listSellers, listBuyers
        # Needs list() to create the double
        self.dinamicListSellers = list(listSellers)
        self.dinamicListBuyers = list(listBuyers)
        self.time = 0
        self.endOfTime = False
        self.maxrounds = maxrounds
        self.echo = echo  # Shows text interface
        self.agent_dict = OrderedDict()

    def moveTime(self):
        if self.endOfTime:
            print("Cannot, end of time")
        else:
            if self.echo:
                print("-- \n")
            self.openMarket()
            self.time += 1

    def restart(self):
        """
        Resets the Market for a second run
        """
        # Needs list() to create the double
        self.dinamicListSellers = list(self.staticListSellers)
        self.dinamicListBuyers = list(self.staticListBuyers)
        self.time = 0
        self.endOfTime = False
        self.agent_dict = OrderedDict()

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
        echo = self.echo  # Shows text interface
        # Update paired status
        seller.paired = buyer.paired = True
        # Exchange mechanism:
        if seller.expectedPrice <= buyer.expectedPrice:
            if echo:
                # Prints traded prices.
                print(str(seller.name) + " and " +
                      str(buyer.name) + " exchange at price " +
                      str(seller.expectedPrice) + "\n")
            # Updates traded status as True
            seller.traded = buyer.traded = True
        else:
            if echo:
                # Prints trade failure
                print(str(seller.name) + " and " +
                      str(buyer.name) + " did not exchange. \n")
            # Updates traded status as False
            seller.traded = buyer.traded = False

    def randomPairing(self, listSellers, listBuyers):
        """
        Gets both the list of sellers and buyers and returns a random paired
        list  always in the shape [[s,b], ...,  [s,b]]
        """
        # Obtiene el largo de las listas
        numSellers = len(listSellers)
        numBuyers = len(listBuyers)

        # Desordena tanto a los compradores como a los vendedores
        listSellers = sample(listSellers, numSellers)  # Shuffles Sellers
        listBuyers = sample(listBuyers, numBuyers)  # Shuffles Buyers

        # Aparea a los que se juntan
        # Zipea con compradores primero si son más que los vendedores
        if numBuyers >= numSellers:
            return list(zip(listSellers, listBuyers))
        else:
            paired = list(zip(listBuyers, listSellers))  # in reverse!
            return [(s, b) for b, s in paired]

    def dinamicUpdater(self, inAgentList):
        """
        All agents that are participating in the market reevaluate their preferences
        And update their price records. Cheks if peak attrition has been reached, 
        and drops the laggers from the market. 
        """
        echo = self.echo
        agentList = list(inAgentList) # Makes a copy

        # Loops in reverse so remove doesn't clash with the iteration pointer
        for agent in agentList:
            # After the trade, both parts re-examin their preferences.
            agent.expect()
            # And updates their price record
            agent.updatePriceRecord()
            # Updates the dinamic lists
            agent.tradedRecord.append(agent.traded)
            agent.pairedRecord.append(agent.paired)
            agent.updateAttrition()
            # If peak endurance reached, remove from list
            if agent.getMeanAttrition() == 1:
                agent.tired = True
                if echo:
                    print(f"Agent {agent.name} quit")
                inAgentList.remove(agent)
            else:
                agent.paired = agent.traded = False  # Prepares next round

    def openMarket(self):
        """
        Main function of the Market object. When the market opens, Sellers and
        Buyers get paired. Then, the exchange mechanism takes place. After that, all
        agents reevaluate their expectations based considering if the trade did happen,
        regardless if they were paired. Then, sellers and buyers both reset their booleans
        for traded and paired to False. Finally, the market checks if the final round has 
        been reached.
        """

        echo = self.echo  # Shows text interface

        # Aparea a los que se juntan
        paired = self.randomPairing(self.dinamicListSellers,
                                    self.dinamicListBuyers)

        if echo:
            # Printea los pares
            print("The Sellers and Buyers paired for time " +
                  str(self.time) + " are ")
            print([(s.name, b.name) for s, b in paired])
            print("\n With expected prices")
            print([(s.expectedPrice, b.expectedPrice) for s, b in paired])

        # Ocurre el mecanismo de mercado
        for pair in paired:
            self.exchangeMechanism(pair)  # Only affects .traded

        # Makes the agent expect, updates their attrition, their prices and
        # decides who is tired and deletes them
        self.dinamicUpdater(self.dinamicListSellers), self.dinamicUpdater(
            self.dinamicListBuyers)
        self.endOfTime = self.checkEndOfTime()

    def checkEndOfTime(self):
        # Checks also for positive amounts of both buyers and sellers
        if (self.dinamicListBuyers and self.dinamicListSellers and
                (self.time < self.maxrounds)):
            return False
        else:
            return True

    def matplotPath(self, agentList, color, alpha):
        for agent in agentList:
            path = agent.priceRecord[:-1]
            # As priceRecord is a variable for t+1, deletes last one (not played)
            tline = [i for i in range(len(path))]
            plt.plot(tline, path, color, alpha=alpha)

    def matplotGraph(self, style='Solarize_Light2', save=False, name=0):
        """" 
        Graphs the price path, the costs and the reserve price for all
        sellers and buyers.

        Requires [style = "style_name"]
        """

        # Sets Style for the graph
        assert style in plt.style.available, NameError
        with plt.style.context(style):

            tmax = self.maxrounds
            t_list = list(range(tmax))

            # Prints the record of expected prices on each round:
            self.matplotPath(self.staticListSellers, '-go', alpha=0.5)
            self.matplotPath(self.staticListBuyers, '-ro', alpha=0.5)

            # Prints bounds
            for s in self.staticListSellers:
                sellerCost = [s.cost for i in t_list]
                plt.plot(t_list, sellerCost, '-g', alpha=0.2)

            for b in self.staticListBuyers:
                buyerEPrice = [b.reservePrice for i in t_list]
                plt.plot(t_list, buyerEPrice, '-r', alpha=0.2)

            # Aestetics
            # Checks for quantities and plurals in static
            numB = len(self.staticListBuyers)
            static_pluralB = 'es' if numB > 1 else ''
            numS = len(self.staticListSellers)
            static_pluralS = 'es' if numS > 1 else ''

            plt.xlabel("Tiempo")
            plt.ylabel("Precios Esperados")
            plt.title(r"Convergencia del precio esperado")

            # Creates the legends with labeling
            # First Legend
            seller = mpatches.Patch(
                color='g', label=f'${numS}$ Vendedor{static_pluralS}')
            buyer = mpatches.Patch(
                color='r', label=f'${numB}$ Comprador{static_pluralB}')
            plt.legend(handles=[seller, buyer],
                       bbox_to_anchor=(1.04, 1), loc="upper left")

            # Creates the remaining counter
            remainingBuyers = len(self.dinamicListBuyers)
            remainingSellers = len(self.dinamicListSellers)
            # Checks for quantities and plurals in dinamic
            dinamic_pluralB = 'es' if numB > 1 else ''
            dinamic_pluralS = 'es' if numS > 1 else ''

            counter = (f"    En $T = {tmax}$\n{remainingSellers} Vendedor{dinamic_pluralS}"
                       f"\n{remainingBuyers} Comprador{dinamic_pluralB}")

            # place a text box in upper left in axes coords

            plt.annotate(counter, xy=(1, .63), xycoords='axes fraction',
                         xytext=(52, 0), textcoords='offset points')

            # Saves File
            if save:
                plt.savefig(str(name), bbox_inches='tight')

            # Plots
            plt.show()         

    def dictMaker(self, sim_id=0):
        """
        Makes an ordered dict from all agents in the market. Repeats
        [Price, Reserve Utiliy, Paired, Traded]
        """
        sim_id = str(sim_id) + "_"

        allAgents = self.staticListSellers + self.staticListBuyers
        self.agent_dict = OrderedDict()
        for agent in allAgents:

            # Unpacks values
            # As priceRecord is a variable for t+1, deletes last one (not played)
            priceList = agent.priceRecord[:-1]
            name = agent.name + "_"
            last_played = min(self.maxrounds, len(agent.pairedRecord))

           # Checks nature of agents
            if isinstance(agent, Seller):
                URes = [agent.cost for i in range(last_played)]
            else:
                URes = [agent.reservePrice for i in range(last_played)]

            # Updates Orderd Dict with agents data
            self.agent_dict.update(
                OrderedDict(
                    {sim_id + name + "Precio": priceList,
                     sim_id + name + "Utilidad Reserva": URes,
                     sim_id + name + "Paired": agent.pairedRecord,
                     sim_id + name + "Traded": agent.tradedRecord
                     }
                )
            )
