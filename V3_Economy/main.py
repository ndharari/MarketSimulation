import os
from collections import OrderedDict
from random import randint
from itertools import chain


import numpy as np
import pandas as pd

import altair as alt
from altair_saver import save

from agents import Buyer, Seller
from market import Market
from graph import *

#CHANGELOG:
"""
- Moved call to graphs to a bulk function

"""

# TODO: Known problems / Future improvements:
"""
- Collect Stability data for multiple endurances
- Think of a plot 
"""

# Simulator function
def simulation(market, N, echo=False, save_pic=False, show_pic=True, save_df=False):
    """Runs the simulation for a given market N times.
       If Echo, prints a Matplotlib graphs

    Arguments:
        market {Market} -- A market object meant to simulate N times
        N {int} -- Number of simulations desired

    Keyword Arguments:
        echo {bool} -- If True, dislpays graphs for each iteration (default: {False})
        save_pic {bool} -- Saves output graph (default: {False})
        save_df {bool} -- Saves output df as csv file (default: {False})

    Returns: A tuple consisting of
        Pandas data frame -- Returns a Data Frame for the simulation of the form:
        [1_Sellers info, 1_Buyer info, ... N+1_Sellers info, N+1_Buyer info]
        Stability data   --
    """
    # Creates the Dicts
    simulation_dict = OrderedDict()
    active_dict = OrderedDict()
    stability_data = [["Name", "T_Sellers", "T_Buyers", "T_max", "Stable", "endurance"]]  

    # Prepares name for files
    num_b = len(market.staticListBuyers)
    num_s = len(market.staticListSellers)
    df_name = f"S{num_s}B{num_b}" # Prepares name of files 
    # Fetches Endurance Data
    e = market.staticListBuyers[0].endurance
    folder = f"{df_name} - endurance = {e}\\"

    for i in range(N):
        while not market.endOfTime:
            market.moveTime()
        
        if echo:
            print(market.endOfTime)

        pic_name = df_name + f" - {i}"

        # Plots the data (For supported styles, plt.style.available)
        market.matplotGraph('Solarize_Light2', save=save_pic, name=pic_name, folder=folder)

        # Keeps the Data
        market.dictMaker(i+1)
        simulation_dict.update(market.agents_dict)

        # Extracts active records
        total_agents = [x + y for x, y in zip (market.active_s_record, market.active_b_record)]
        active_dict[i+1] = total_agents


        # Extracts stability data [id, T_sellers, T_buyers, T_max, Stable, Endurance]
        current_stab = [i+1, 
        market.active_s_record[-1],
        market.active_b_record[-1],
        market.time,
        market.time<market.maxrounds,
        market.staticListSellers[0].endurance]

        stability_data.append(current_stab)

        # Restarts everything
        for agent in chain(listSellers, listBuyers):
            agent.restart()
        market.restart()

    sim_df = pd.DataFrame(dict([(key, pd.Series(value)) 
                                for key, value 
                                in simulation_dict.items()]))

    stab_df = pd.DataFrame(stability_data[1:], 
                           columns=stability_data[0]).set_index("Name")

    active_df = pd.DataFrame(dict([(key, pd.Series(value)) 
                                for key, value 
                                in active_dict.items()]))
        
    # For supported styles, plt.style.available
    
    if save_df:
        sim_df.to_csv(f".\\output\\{folder}Round Data for {df_name}.csv")
        stab_df.to_csv(f".\\output\\{folder}Stability for {df_name}.csv")
        active_df.to_csv(f".\\output\\{folder}Active Agents for {df_name}.csv")

    return sim_df, stab_df, active_df

# Sets the Parameters
save_pic, save_df, echo = False, True, False
num_s, num_b = 3, 3 
endurance = 4
name = f"S{num_s}B{num_b}"
folder = f"{name} - endurance = {endurance}\\"


# Sets up everything
listSellers = [Seller(i, 10, 20, endurance=endurance, delta=0.5) for i in range(num_s)]
listBuyers = [Buyer(i, 30, 40, endurance=endurance, delta=0.5) for i in range(num_b)]
market = Market(listSellers, listBuyers, t_low = 20, maxrounds=150, echo=echo)

# Runs the simulations
simulation_df, stab_df, active_df = simulation(market, 200, echo=echo,
                                    save_pic=save_pic, save_df=save_df)


alt.data_transformers.disable_max_rows() # For Plotting porpuse
# Prints all main graphs
bulk_alt(simulation_df, stab_df, echo=echo, save=save_pic, folder=folder)

# Stability Plots
stacked_hist(active_df, endurance, echo=echo, save=save_pic, folder=folder)


