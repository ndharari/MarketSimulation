from collections import OrderedDict

import pandas as pd

from agents import Buyer, Seller
from market import Market

# TODO: Known problems / Future improvements:
"""
- Change graphical interphace to Altair/Seaborn
- Program the overall checks
- Program the endurance checks
"""


def simulation(market, N, echo=False):
    """Runs the simulation for a given market N times.

    Arguments:
        market {Market} -- A market object meant to simulate N times
        N {int} -- Number of simulations desired

    Keyword Arguments:
        echo {bool} -- If True, dislpays graphs for each iteration (default: {False})

    Returns:
        Matplotlib graph -- If echo, returns the matplotñlib graph of the simulation
        Pandas data frame -- Returns a Data Frame for the simulation of the form:
        [1_Sellers info, 1_Buyer info, ... N+1_Sellers info, N+1_Buyer info]
    """

    simulation_dict = OrderedDict()  # Creates the Dict

    for i in range(N):
        while not market.endOfTime:
            market.moveTime()
        print(market.endOfTime)

        # For supported styles, plt.style.available
        if echo:
            market.matplotGraph('Solarize_Light2')

        # Keeps the Data
        market.dictMaker(i+1)
        simulation_dict.update(market.agent_dict)

        # Restarts everything

        for seller in listSellers:
            seller.restart()

        for buyer in listBuyers:
            buyer.restart()
        market.restart()

    return pd.DataFrame(dict([(key, pd.Series(value)) for key, value in simulation_dict.items()]))


# Sets up everything
listSellers = [Seller(i, 10, 20, tipe="delta") for i in range(4)]
listBuyers = [Buyer(i, 20, 30, tipe="delta") for i in range(1)]
market = Market(listSellers, listBuyers, 50, echo=True)

# Runs the simulations
simulation_df = simulation(market, 1, echo=True)

simulation_df.filter(regex="1_B_._Paired")
simulation_df.filter(regex="1_._._Traded")

simulation_df
