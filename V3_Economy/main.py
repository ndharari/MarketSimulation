from collections import OrderedDict

import pandas as pd

import altair as alt

from agents import Buyer, Seller
from market import Market

# TODO: Known problems / Future improvements:
"""
- Change graphical interphace to Altair/Seaborn
- Program the overall checks
- Program the endurance checks
- Change index to time
- In Heymann Graph extend all Ures until the end
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
listSellers = [Seller(i, 10, 20, endurance=3, delta=0.5) for i in range(2)]
listBuyers = [Buyer(i, 20, 30, endurance=3, delta=0.5) for i in range(1)]
market = Market(listSellers, listBuyers, 50, echo=False)

# Runs the simulations
simulation_df = simulation(market, 10, echo=True)


# Heymann et al style graph
def heymann(dataFrame, side="S"):
    """ Graphs an aggregated style graph like the one found in Heymann et al 2014

    Arguments:
        dataFrame {Pandas Data Frame} -- The simulation Data Frame

    Keyword Arguments:
        side {str} -- Buyer ("B") or Seller ("S") (default: {"S"})

    Returns:
        output -- Altair **interactive** graph
    """

    plot_df = pd.DataFrame()

    assert (side == "S" or side == "B"), 'Side must be S or B'

    # Sets regex expression
    reg = "{}_._Precio".format(side)

    # Gets max, min, avg and a sample for column
    plot_df['max'] = dataFrame.filter(regex=reg).max(axis=1)
    plot_df['min'] = dataFrame.filter(regex=reg).min(axis=1)
    plot_df['avg'] = dataFrame.filter(regex=reg).mean(axis=1)
    plot_df['sample'] = dataFrame.filter(regex=reg).sample(1, axis=1)
    plot_df.index.names = ['time']

    # Gets all URes (only first simulation)
    # Uses .fillna(dataFrame.mean() to extend the lineall the way through
    ures_df = dataFrame.filter(regex="^(1_)._._Utilidad Reserva").fillna(dataFrame.mean())
    ures_df.index.names = ['time']
    ures_df = ures_df.reset_index()
    # Melts the dataframe for Altair
    ures_df = ures_df.melt("time")
    # Sets tipo so altair doesn't mix up observations. Remember: Altair divides lines by colour
    ures_df['tipo'] = ['S' if 'S' in x else 'B' for x in ures_df['variable']]

    # Makes the graph.
    # Data in wide-form, must make several graphs
    base = alt.Chart(plot_df.reset_index()).mark_line().encode(x="time:Q")

    no_ures = alt.layer(
        base.mark_line(color='#BC2D30').encode(y=alt.Y('max:Q',
                                                       scale=alt.Scale(zero=False))),

        base.mark_line(color='#6F3D79').encode(y=alt.Y('min:Q',
                                                       scale=alt.Scale(zero=False))),

        base.mark_point(color='#2E578C').encode(y=alt.Y('avg:Q',
                                                        scale=alt.Scale(zero=False))),

        base.mark_line(color='#E7A13D').encode(y=alt.Y('sample:Q',
                                                       scale=alt.Scale(zero=False))),
    ).interactive().properties(title='Simulaciones')

    ures = alt.Chart(ures_df).mark_line(opacity=0.4).encode(
        x="time:Q",
        y=alt.Y('value:Q',
                scale=alt.Scale(zero=False)),
        detail='variable',
        color=alt.Color('tipo',
                        scale=alt.Scale(
                            domain=['S', 'B'],
                            range=['green', 'red'])))

    return no_ures + ures


heymann_graph = heymann(simulation_df, "S")
heymann_graph


simulation_df
