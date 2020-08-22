import os
from collections import OrderedDict
from random import randint

import numpy as np
import pandas as pd
import altair as alt
from altair_saver import save

from agents import Buyer, Seller
from market import Market
from graph import heymann, following_sample, avg_vs_avg, intra_inter

#CHANGELOG:
"""
- Meassure turn by turn "representative mean agent" 
- Track the slope of the best fit line for the representative agent in a 10 turn window. 
- Check stability defined as n consecutive turns with a slope < epsilon.
- Run simulationn for at least T_low turns. End simulation either if stable condition is reached or if T_high is reached.
- Added stability agregator
- Added stability boxplot to graphs
"""

# TODO: Known problems / Future improvements:
"""
- Do stats magic to stability
"""

# Simulator function
def simulation(market, N, echo=False, save_pic=False, save_df=False):
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
    stability_data = [["Name", "T_Sellers", "T_Buyers", "T_max", "Stable", "endurance"]]  

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

        # Extracts stability data [id, T_sellers, T_buyers, T_max, Stable, Endurance]
        current_stab = [i+1, 
        market.active_s_record[-1],
        market.active_b_record[-1],
        market.time,
        market.time<market.maxrounds,
        market.staticListSellers[0].endurance]

        stability_data.append(current_stab)

        # Restarts everything
        for seller in listSellers:
            seller.restart()

        for buyer in listBuyers:
            buyer.restart()
        market.restart()

    sim_df = pd.DataFrame(dict([(key, pd.Series(value)) 
                                for key, value 
                                in simulation_dict.items()]))

    stab_df = pd.DataFrame(stability_data[1:], 
                           columns=stability_data[0]).set_index("Name")
        
    # For supported styles, plt.style.available
    if save_df:
        sim_df.to_csv(f".\\output\\Round Data for {df_name}.csv")
        stab_df.to_csv(f".\\output\\Stability for {df_name}.csv")

    
    return sim_df, stab_df

save_pic, save_df, echo = False, True, False
pic_echo = True

# Sets up everything
listSellers = [Seller(i, 10, 20, endurance=3, delta=0.5) for i in range(3)]
listBuyers = [Buyer(i, 30, 40, endurance=3, delta=0.5) for i in range(3)]
market = Market(listSellers, listBuyers, t_low = 20, maxrounds=150, echo=echo)

# Runs the simulations
simulation_df, stab_df = simulation(market, 100, echo=echo, save_pic=save_pic, save_df=save_df)

alt.data_transformers.disable_max_rows() # For Plotting porpuse

# Makes the Heymann et al style graph
heymann(simulation_df, stab_df, "S", echo=pic_echo, save=save_pic)
heymann(simulation_df, stab_df, "B", echo=pic_echo, save=save_pic)

# Aggregates and follows a sample agent
following_sample(simulation_df, stab_df, "S", 0, echo=pic_echo, save=save_pic)
following_sample(simulation_df, stab_df, "B", 0, echo=pic_echo, save=save_pic)

# Aggregates and follows all agents
avg_vs_avg(simulation_df, stab_df, echo=pic_echo, save=save_pic)

# Aggregates and follows all agents
intra_inter(simulation_df, stab_df, "S", echo=pic_echo, save=save_pic)
intra_inter(simulation_df, stab_df, "B", echo=pic_echo, save=save_pic)

