from collections import OrderedDict
from random import randint

import pandas as pd

import altair as alt
from altair_saver import save

from agents import Buyer, Seller
from market import Market

# TODO: Known problems / Future improvements:
"""
- Program the endurance checks
- Add survivors aggregators and graphers
"""

alt.data_transformers.disable_max_rows() # For Plotting porpuse

# Simulator function
def simulation(market, N, echo=False, save=False):
    """Runs the simulation for a given market N times.

    Arguments:
        market {Market} -- A market object meant to simulate N times
        N {int} -- Number of simulations desired

    Keyword Arguments:
        echo {bool} -- If True, dislpays graphs for each iteration (default: {False})
        save {bool} -- Saves output graph (default: {False})

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
            market.matplotGraph('Solarize_Light2', save=True, name=i)

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

# Heymann et al style graph
def heymann(dataFrame, side="S", style='opaque', save=False):
    """ Graphs an aggregated style graph like the one found in Heymann et al 2014

    Arguments:
        dataFrame {Pandas Data Frame} -- The simulation Data Frame

    Keyword Arguments:
        side {str} -- Buyer ("B") or Seller ("S") (default: {"S"})
        stryle {str} -- Styler for altair themes

    Returns:
        output -- Altair **interactive** graph
    """

    plot_df = pd.DataFrame()

    assert (side == "S" or side == "B"), 'Side must be S or B'

    # Sets regex expression
    reg = f"{side}_._Precio"

    # Gets max, min, avg and a sample for column
    plot_df['max'] = dataFrame.filter(regex=reg).max(axis=1)
    plot_df['min'] = dataFrame.filter(regex=reg).min(axis=1)
    plot_df['avg'] = dataFrame.filter(regex=reg).mean(axis=1)
    plot_df['sample'] = dataFrame.filter(regex=reg).sample(1, axis=1)
    plot_df.index.names = ['time']

    # Gets all URes (only first simulation)
    # Uses .fillna(dataFrame.mean() to extend the lineall the way through
    ures_df = dataFrame.filter(
        regex="^(1_)._._Utilidad Reserva").fillna(dataFrame.mean())
    ures_df.index.names = ['time']
    ures_df = ures_df.reset_index()
    # Melts the dataframe for Altair
    ures_df = ures_df.melt("time")
    # Sets tipo so altair doesn't mix up observations. Remember: Altair divides lines by colour
    ures_df['tipo'] = ['S' if 'S' in x else 'B' for x in ures_df['variable']]

    # Makes the graph.
    # Data in wide-form, must make several graphs
    with alt.themes.enable(style):

        base = alt.Chart(plot_df.reset_index()).mark_line().encode(x="time:Q")

        no_ures = alt.layer(
            base.mark_line(color='#BC2D30').encode(y=alt.Y('max:Q',
                                                           scale=alt.Scale(zero=False))),

            base.mark_line(color='#6F3D79').encode(y=alt.Y('min:Q',
                                                           scale=alt.Scale(zero=False))),

            base.mark_point(color='#2E578C', opacity=0.6).encode(y=alt.Y('avg:Q',
                                                                         scale=alt.Scale(zero=False))),

            base.mark_line(color='#E7A13D').encode(y=alt.Y('sample:Q',
                                                           scale=alt.Scale(zero=False))),
        ).properties(title=f'Heymann et al Graph for {"Seller" if side == "S" else "Buyer"}')

        ures = alt.Chart(ures_df).mark_line(opacity=0.3).encode(
            x="time:Q",
            y=alt.Y('value:Q',
                    scale=alt.Scale(zero=False)),
            detail='variable',
            color=alt.Color('tipo',
                            scale=alt.Scale(
                                domain=['S', 'B'],
                                range=['green', 'red'])))
    chart = no_ures + ures
    if save:
        chart.save(f'Heymann {side}.svg')
    return chart

# Sample following
def following_sample(dataFrame, side="S", name=0, style='opaque', save=False):
    """ Graphs all the expected prices of an agent and its averages

    Arguments:
        dataFrame {Pandas Data Frame} -- The simulation Data Frame

    Keyword Arguments:
        side {str} -- Buyer ("B") or Seller ("S") (default: {"S"})
        name {int} -- The ith agent meant to sample (default: {"0"})
        stryle {str} -- Styler for altair themes

    Returns:
        output -- Altair **interactive** graph
    """

    plot_df = pd.DataFrame()
    ures_df = pd.DataFrame()

    assert (side == "S" or side == "B"), 'Side must be S or B'

    # Sets regex expression
    reg1 = f"{side}_{name}_Precio"

    # Gets all iterations to a melted pd.dataFrame
    plot_df = dataFrame.filter(regex=reg1)
    plot_df = plot_df.assign(avg=plot_df.mean(axis=1))
    plot_df.index.names = ['time']
    plot_df = plot_df.reset_index()
    plot_df = plot_df.melt("time")
    plot_df['tipo'] = ['P' if 'P' in x else 'avg' for x in plot_df['variable']]

    # Gets all URes (only first simulation)
    # Uses .fillna(dataFrame.mean() to extend the lineall the way through
    ures_df = dataFrame.filter(regex="^(1_)._._Uti").fillna(dataFrame.mean())
    ures_df.index.names = ['time']
    ures_df = ures_df.reset_index()
    # Melts the dataframe for Altair
    ures_df = ures_df.melt("time")
    # Sets tipo so altair doesn't mix up observations. Remember: Altair divides lines by colour
    ures_df['tipo'] = ['S' if 'S' in x else 'B' for x in ures_df['variable']]

    # Makes the graph.
    # Data in wide-form, must make several graphs
    with alt.themes.enable(style):

        base = alt.Chart(plot_df).mark_line(opacity=0.6).encode(
            x="time:Q",
            y=alt.Y('value:Q',
                    scale=alt.Scale(zero=False)),
            detail='variable',
            color=alt.Color('tipo',
                            scale=alt.Scale(
                                domain=['S', 'B', 'P', 'avg'],
                                range=['green', 'red', '#2E578C', '#E7A13D']))
        )

        ures = alt.Chart(ures_df).mark_line(opacity=0.3).encode(
            x="time:Q",
            y=alt.Y('value:Q',
                    scale=alt.Scale(zero=False)),
            detail='variable',
            color=alt.Color('tipo',
                            scale=alt.Scale(
                                domain=['S', 'B'],
                                range=['green', 'red', '#2E578C', '#E7A13D']))
        ).properties(
            title=f'Following a sample agent {"Seller" if side == "S" else "Buyer"}')

    chart = base + ures
    if save:
        chart.save(f'Follow {side}.svg')
    return chart

# Overall Average of sellers and buyers
def avg_vs_avg(dataFrame, style='opaque', save=False):
    """ Graphs an aggregated style graph showing Avg Price vs Avg Price

    Arguments:
        dataFrame {Pandas Data Frame} -- The simulation Data Frame

    Keyword Arguments:
        stryle {str} -- Styler for altair themes

    Returns:
        output -- Altair **interactive** graph
    """

    plot_df = pd.DataFrame()
    ures_df = pd.DataFrame()

    # Gets all iterations to a melted pd.dataFrame
    plot_df['Avg Seller'] = dataFrame.filter(regex="S_._Precio").mean(axis=1)
    plot_df['Avg Buyer'] = dataFrame.filter(regex="B_._Precio").mean(axis=1)
    plot_df.index.names = ['time']
    plot_df = plot_df.reset_index()
    plot_df = plot_df.melt("time")

    # Gets all URes (only first simulation)
    # Uses .fillna(dataFrame.mean() to extend the lineall the way through
    ures_df = dataFrame.filter(regex="^(1_)._._Uti").fillna(dataFrame.mean())
    ures_df.index.names = ['time']
    ures_df = ures_df.reset_index()
    # Melts the dataframe for Altair
    ures_df = ures_df.melt("time")
    # Sets tipo so altair doesn't mix up observations. Remember: Altair divides lines by colour
    ures_df['tipo'] = ['S' if 'S' in x else 'B' for x in ures_df['variable']]

    # Makes the graph.
    # Data in wide-form, must make several graphs
    with alt.themes.enable(style):

        base = alt.Chart(plot_df).mark_line(opacity=0.6).encode(
            x="time:Q",
            y=alt.Y('value:Q',
                    scale=alt.Scale(zero=False)),
            color=alt.Color('variable',
                            scale=alt.Scale(
                                domain=['S', 'B', 'Avg Seller', 'Avg Buyer'],
                                range=['green', 'red', '#2E578C', '#E7A13D']))
        )

        ures = alt.Chart(ures_df).mark_line(opacity=0.3).encode(
            x="time:Q",
            y=alt.Y('value:Q',
                    scale=alt.Scale(zero=False)),
            detail='variable',
            color=alt.Color('tipo',
                            scale=alt.Scale(
                                domain=['S', 'B'],
                                range=['green', 'red', '#2E578C', '#E7A13D']))
        ).properties(title=f'Avg vs Avg across simulations')
    
    chart = base + ures

    if save:
        chart.save(f'avg vs avg.svg', scale_factor=2.0)
    return chart

# Inter_intra comparison
def intra_inter(dataFrame, side="S", style='opaque', save=False):
    """ Graphs an aggregated style graph showing the average between each simulation

    Arguments:
        dataFrame {Pandas Data Frame} -- The simulation Data Frame
        num {int} -- The number of simulations


    Keyword Arguments:
        side {str} -- Buyer ("B") or Seller ("S") (default: {"S"})
        stryle {str} -- Styler for altair themes

    Returns:
        output -- Altair **interactive** graph
    """
    plot_df=pd.DataFrame()
    ures_df=pd.DataFrame()
    assert (side == "S" or side == "B"), 'Side must be S or B'
    # Gets the number of simulations
    sim_str=dataFrame.columns[-1]
    place=sim_str.find("_")
    sim_num=int(sim_str[:place])
    # Gets the overall average:
    plot_df['Overall']=dataFrame.filter(regex=f"{side}_._Precio").mean(axis=1)
    # Gets the average in each iteration:
    for i in range(sim_num):
        reg=f"{i}_{side}_._Precio"
        plot_df[f'Avg {i}']=dataFrame.filter(regex=reg).mean(axis=1)
    plot_df.index.names=['time']
    plot_df=plot_df.reset_index()
    plot_df=plot_df.melt("time")
    plot_df['tipo']=[
        'Avg' if 'Avg' in x else "Overall" for x in plot_df['variable']]
    # Gets all URes (only first simulation)
    # Uses .fillna(dataFrame.mean() to extend the lineall the way through
    ures_df=dataFrame.filter(regex="^(1_)._._Uti").fillna(dataFrame.mean())
    ures_df.index.names=['time']
    ures_df=ures_df.reset_index()
    # Melts the dataframe for Altair
    ures_df=ures_df.melt("time")
    # Sets tipo so altair doesn't mix up observations. Remember: Altair divides lines by color
    ures_df['tipo']=['S' if 'S' in x else 'B' for x in ures_df['variable']]
    # Makes the graph.
    # Data in wide-form, must make several graphs
    with alt.themes.enable(style):
        base=alt.Chart(plot_df).mark_line(opacity=0.6).encode(
            x="time:Q",
            y=alt.Y('value:Q',
                    scale=alt.Scale(zero=False)),
            detail='variable',
            color=alt.Color('tipo',
                            scale=alt.Scale(
                                domain=['S', 'B', 'Avg', 'Overall'],
                                range=['green', 'red', '#2E578C', 'magenta']))
        )
        ures=alt.Chart(ures_df).mark_line(opacity=0.3).encode(
            x="time:Q",
            y=alt.Y('value:Q',
                    scale=alt.Scale(zero=False)),
            detail='variable',
            color=alt.Color('tipo',
                            scale=alt.Scale(
                                domain=['S', 'B', 'avg', 'Overall'],
                                range=['green', 'red', '#2E578C', '#E7A13D']))
        ).properties(title='Avg prices between simulations '  
        f'and overall from {"Seller" if side == "S" else "Buyer"}')
    chart=base + ures
    if save:
        chart.save(f'Inter-Intra {side}.svg', scale_factor=2.0)
    return chart


# Sets up everything
listSellers=[Seller(i, 10, 20, endurance=50, delta=0.5) for i in range(10)]
listBuyers=[Buyer(i, 20, 30, endurance=50, delta=0.5) for i in range(1)]
market=Market(listSellers, listBuyers, 50, echo=False)

# Runs the simulations
simulation_df=simulation(market, 100, echo=True)


# Makes the Heymann et al style graph
heymann(simulation_df, "S", save=True)
heymann(simulation_df, "B", save=True)


# Aggregates and follows a sample agent
following_sample(simulation_df, "S", 0, save=True)
following_sample(simulation_df, "B", 0, save=True)

# Aggregates and follows all agents
avg_vs_avg(simulation_df, save=True)


# Aggregates and follows all agents
intra_inter(simulation_df, "S", save=True)
intra_inter(simulation_df, "B", save=True)


# TODO: grafico tipo avg vs avg  pero dividido en deciles
