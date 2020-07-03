import os
from collections import OrderedDict
from random import randint

import pandas as pd
import altair as alt
from altair_saver import save

from agents import Buyer, Seller
from market import Market
from graph import heymann, following_sample, avg_vs_avg, intra_inter

# TODO: Known problems / Future improvements:
"""
- Program the endurance checks
- Add survivors aggregators and graphers
- Add standard deviation agregator for prices
- (Maybe) let simulation run until sd is necesarily
"""

# Simulator function
def simulation(market, N, echo=False, save_pic=False, save_df=False):
    """Runs the simulation for a given market N times.

    Arguments:
        market {Market} -- A market object meant to simulate N times
        N {int} -- Number of simulations desired

    Keyword Arguments:
        echo {bool} -- If True, dislpays graphs for each iteration (default: {False})
        save_pic {bool} -- Saves output graph (default: {False})
        save_df {bool} -- Saves output df as csv file (default: {False})

    Returns:
        Matplotlib graph -- If echo, returns the matplotñlib graph of the simulation
        Pandas data frame -- Returns a Data Frame for the simulation of the form:
        [1_Sellers info, 1_Buyer info, ... N+1_Sellers info, N+1_Buyer info]
    """

    simulation_dict = OrderedDict()  # Creates the Dict
    # Prepares name for files
    num_b = len(market.staticListBuyers)
    num_s = len(market.staticListSellers)
    df_name = f"S{num_s}B{num_b}" # Prepares name of files 

    for i in range(N):
        while not market.endOfTime:
            market.moveTime()
        
        if echo:
            print(market.endOfTime)

        pic_name = df_name + f" - {i}"

        # For supported styles, plt.style.available
        market.matplotGraph('Solarize_Light2', save=save_pic, name=pic_name)

        # Keeps the Data
        market.dictMaker(i+1)
        simulation_dict.update(market.agents_dict)

        # Restarts everything

        for seller in listSellers:
            seller.restart()

        for buyer in listBuyers:
            buyer.restart()
        market.restart()

    sim_df = pd.DataFrame(dict([(key, pd.Series(value)) 
                                for key, value 
                                in simulation_dict.items()]))
        
    # For supported styles, plt.style.available
    if save_df:
        sim_df.to_csv(f".\\output\\{df_name}.csv")
    
    return sim_df

# Sets up everything
listSellers = [Seller(i, 10, 20, endurance=5, delta=0.5) for i in range(3)]
listBuyers = [Buyer(i, 20, 30, endurance=5, delta=0.5) for i in range(3)]
market = Market(listSellers, listBuyers, 50, echo=False)

# Runs the simulations
simulation_df = simulation(market, 20, echo=False, save_pic=True, save_df=True)

simulation_df

alt.data_transformers.disable_max_rows() # For Plotting porpuse

# Makes the Heymann et al style graph
heymann(simulation_df, "S", echo=True, save=True)
heymann(simulation_df, "B", echo=True, save=True)

# Aggregates and follows a sample agent
following_sample(simulation_df, "S", 0, echo=True, save=True)
following_sample(simulation_df, "B", 0, echo=True, save=True)

# Aggregates and follows all agents
avg_vs_avg(simulation_df, echo=True, save=True)

# Aggregates and follows all agents
intra_inter(simulation_df, "S", echo=True, save=True)
intra_inter(simulation_df, "B", echo=True, save=True)

