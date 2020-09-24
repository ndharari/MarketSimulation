import os
from collections import OrderedDict
from random import randint
from itertools import chain

import numpy as np
import pandas as pd

import altair as alt
from altair_saver import save
alt.data_transformers.disable_max_rows() # For Plotting porpuse

from agents import Buyer, Seller
from market import Market
from graph import *

s_b_configs = [[3, 3], [4, 3], [3, 4], [5, 3], [6, 3], [5, 5]]
endurances = [3, 4, 5, 6]


# Simulator function
def large_simulator(market, N, save_df=False):
    
    # Creates the Dicts
    active_dict = OrderedDict()
    stability_data = [["Name", "Config", "T_max", "Stable", "endurance"]]

    if not os.path.exists(f".\\output\\Large"):
        os.mkdir(f".\\output\\Large")   

    # Prepares name for files
    num_b = len(market.staticListBuyers)
    num_s = len(market.staticListSellers)
    e = market.staticListBuyers[0].endurance
    df_name = f"S{num_s}B{num_b}-E{e}" # Prepares name of files
    
    for i in range(N):
        while not market.endOfTime:
            market.moveTime()

        # Extracts active records
        total_agents = [f"{x}S-{y}B" for x, y in zip(market.active_s_record, 
                                                        market.active_b_record)]
        active_dict[i+1] = total_agents

        # Extracts stability data [id, Config, T_max, Stable, Endurance]
        current_stab = [i+1, 
        f"{market.active_s_record[-1]}S-{market.active_b_record[-1]}B",
        market.time,
        market.time<market.maxrounds,
        market.staticListSellers[0].endurance]
        stability_data.append(current_stab)

        # Restarts everything
        for agent in chain(ls, lb):
            agent.restart()
        market.restart()

    stab_df = pd.DataFrame(stability_data[1:], 
                           columns=stability_data[0]).set_index("Name")

    active_df = pd.DataFrame(dict([(key, pd.Series(value)) 
                                for key, value 
                                in active_dict.items()]))
        
    if save_df:
        stab_df.to_csv(f".\\output\\Large\\Stab {df_name}.csv")
        active_df.to_csv(f".\\output\\Large\\AA {df_name}.csv")

    return stab_df, active_df


# Seteas las listas con un endurance cualquiera
for pair in s_b_configs:
    num_s, num_b = pair[0], pair[1]
    ls = [Seller(i, 10, 20, endurance=0, delta=0.5) for i in range(num_s)]
    lb = [Buyer(i, 30, 40, endurance=0, delta=0.5) for i in range(num_b)]
    market = Market(ls, lb, t_low = 20, maxrounds=500, echo=False)
    
    # Sets the correct endurances
    for e in endurances:
        for agent in chain(ls, lb):
            agent.endurance = e
            agent.change_endurance()
        # Sets the name of the file
        df_name = f"S{num_s}B{num_b}-E{e}"

        # Runs the simulations
        stab_df, active_df = large_simulator(market, 1000, save_df=True)
        
        # First Graph: Active agents!
        # Prepares the data Frame    
        active_df.index.names = ['time']
        active_df = active_df.reset_index()
        # Melts the dataframe for Altair
        active_df = active_df.melt("time")
        active_df.dropna(inplace= True)

        # First Graph
        output = alt.Chart(active_df).mark_bar().encode(
        x=alt.X('time:Q', title="Tiempo"),
        y=alt.Y('count(value)', title="Simulaciones"),
        color= alt.Color('value:O', legend=alt.Legend(title="Configuraciones",
                                                      columns = 4),
                        scale=alt.Scale(scheme="turbo"))
        ).properties(
            title=f'Numero de simulaciones con cada configuración. Endurance = {e}',
            height=70
            )
        print(df_name)
        output.save(f".\\output\\Large\\N sim for {df_name}.html")
    
        # Second Graph: Stability! 
        bars = alt.Chart(stab_df).mark_bar().encode(
            x=alt.X('T_max:Q', title="Estabilidad alcanzada", 
            bin=alt.Bin(step=5)),
            y=alt.Y('count()', title="Simulaciones"),
            color= alt.Color('Config:O', legend=alt.Legend(title="Configuraciones",
                                                            columns= 4),
                        scale=alt.Scale(scheme="turbo")
        )
        ).properties(title=f'Configuraciones al alcanzar estabilidad. Endurance = {e}',
            height=70)
        bars.save(f".\\output\\Large\\Stab {df_name}.html")
        
        



