import os
import errno
import altair as alt
import pandas as pd
from altair_saver import save


def stab_hist(dataFrame):

    bars = alt.Chart(dataFrame).mark_bar().encode(
        x=alt.X('T_max:Q', title="Estabilidad alcanzada", 
         bin=alt.Bin(step=5)),
        y=alt.Y('count()', axis=None)
    )

    text = bars.mark_text(
        align='center',
        baseline='top',
        dy=-10  # Nudges text to up a little
    ).encode(
        text='count()'
    )

    return (bars + text).properties(height=50)


def stab_boxplt(dataFrame):
    output = alt.Chart(dataFrame).mark_boxplot(
        box = alt.MarkConfig(opacity=.7), 
        median=alt.MarkConfig(color="Black")).encode(
        x=alt.X('T_max:Q', title="Estabilidad alcanzada"),
    )
    return output

# Heymann et al style graph
def heymann(dataFrame, stab, side="S", style='opaque', echo=False, save=False):
    """ Graphs an aggregated style graph like the one found in Heymann et al 2014

    Arguments:
        dataFrame {Pandas Data Frame} -- The simulation Data Frame

    Keyword Arguments:
        side {str} -- Buyer ("B") or Seller ("S") (default: {"S"})
        stryle {str} -- Styler for altair themes

    Returns (if echo):
        output -- Altair **interactive** graph
    """
    
    # Checks if chromedriver is in directory for saving
    if save and not os.path.isfile('./chromedriver.exe'):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), 
                                'chromedriver.exe')

    plot_df = pd.DataFrame()

    assert (side == "S" or side == "B"), 'Side must be S or B'

    # Sets regex expression
    reg = f"{side}_._Precio"

    # Gets max, min, avg and a sample for column
    plot_df['max'] = dataFrame.filter(regex=reg).max(axis=1)
    plot_df['min'] = dataFrame.filter(regex=reg).min(axis=1)
    plot_df['media'] = dataFrame.filter(regex=reg).mean(axis=1)
    plot_df['muestra'] = dataFrame.filter(regex=reg).sample(1, axis=1)
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
            base.mark_line(color='#BC2D30', opacity=0.8).encode(
                y=alt.Y('max:Q',
                        scale=alt.Scale(zero=False))
            ),

            base.mark_line(color='#6F3D79', opacity=0.7).encode(
                y=alt.Y('min:Q',
                        scale=alt.Scale(zero=False))
            ),

            base.mark_point(color='#2E578C', opacity=0.6).encode(
                y=alt.Y('media:Q',
                        scale=alt.Scale(zero=False))
            ),

            base.mark_line(color='#E7A13D', opacity=0.8).encode(
                y=alt.Y('muestra:Q',
                        scale=alt.Scale(zero=False))
            )
        ).properties(title='Grafico estilo Heymann et al (2014) '
         f'para {"Vendedores" if side == "S" else "Compradores"}'
         )

        ures = alt.Chart(ures_df).mark_line(opacity=0.3).encode(
            x=alt.X('time:Q', title="Tiempo"),
            y=alt.Y('value:Q',title="Precio maximo, minimo, medio y muestra",
                    scale=alt.Scale(zero=False)),
            detail='variable',
            color=alt.Color('tipo', legend=alt.Legend(title="Indicadores"),
                            scale=alt.Scale(
                                domain=['S', 'B'],
                                range=['green', 'red'])))
    chart = no_ures + ures
    output = (chart & stab_hist(stab)).resolve_scale(x='shared').configure_axis(
                    grid=False
                    )
    if save:
        output.save(f'.\\output\\Heymann {side}.svg')
    if echo:
            return output

# Sample following
def following_sample(dataFrame, stab, side="S", name=0, style='opaque', echo=False, save=False):
    """ Graphs all the expected prices of an agent and its averages

    Arguments:
        dataFrame {Pandas Data Frame} -- The simulation Data Frame

    Keyword Arguments:
        side {str} -- Buyer ("B") or Seller ("S") (default: {"S"})
        name {int} -- The ith agent meant to sample (default: {"0"})
        stryle {str} -- Styler for altair themes

    Returns (if echo):
        output -- Altair **interactive** graph
    """

    # Checks if chromedriver is in directory for saving
    if save and not os.path.isfile('./chromedriver.exe'):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), 
                                'chromedriver.exe')

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
    plot_df['tipo'] = ['P' if 'P' in x else 'Media' for x in plot_df['variable']]

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
                                domain=['S', 'B', 'P', 'Media'],
                                range=['green', 'red', '#2E578C', '#E7A13D']))
        )

        ures = alt.Chart(ures_df).mark_line(opacity=0.3).encode(
            x=alt.X('time:Q', title="Tiempo"),
            y=alt.Y('value:Q', title="Precio Esperado", 
                    scale=alt.Scale(zero=False)),
            detail='variable',
            color=alt.Color('tipo', legend=alt.Legend(title="Indicadores"),
                            scale=alt.Scale(
                                domain=['S', 'B'],
                                range=['green', 'red', '#2E578C', '#E7A13D']))
        ).properties(
            title=f'Recorrido de un {"vendedor" if side == "S" else "comprador"} al azar'
            )
    chart = base + ures
    output = (chart & stab_hist(stab)).resolve_scale(x='shared').configure_axis(
                    grid=False
                    )

    if save:
        output.save(f'.\\output\\Follow {side}.svg')
    if echo:
            return output

# Overall Average of sellers and buyers
def avg_vs_avg(dataFrame, stab, style='opaque', echo=False, save=False):
    """ Graphs an aggregated style graph showing Avg Price vs Avg Price

    Arguments:
        dataFrame {Pandas Data Frame} -- The simulation Data Frame

    Keyword Arguments:
        stryle {str} -- Styler for altair themes

    Returns (if echo):
        output -- Altair **interactive** graph
    """

    # Checks if chromedriver is in directory for saving
    if save and not os.path.isfile('./chromedriver.exe'):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), 
                                'chromedriver.exe')

    plot_df = pd.DataFrame()
    ures_df = pd.DataFrame()

    # Gets all iterations to a melted pd.dataFrame
    plot_df['Media S'] = dataFrame.filter(regex="S_._Precio").mean(axis=1)
    plot_df['Media B'] = dataFrame.filter(regex="B_._Precio").mean(axis=1)
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
                                domain=['S', 'B', 'Media S', 'Media B'],
                                range=['green', 'red', '#2E578C', '#E7A13D']))
        )

        ures = alt.Chart(ures_df).mark_line(opacity=0.3).encode(
            x=alt.X('time:Q', title="Tiempo"),
            y=alt.Y('value:Q', title="Precio Esperado",
                    scale=alt.Scale(zero=False)),
            detail='variable',
            color=alt.Color('tipo', legend=alt.Legend(title="Indicadores"),
                            scale=alt.Scale(
                                domain=['S', 'B'],
                                range=['green', 'red', '#2E578C', '#E7A13D']))
        ).properties(title=f'Media vs media a lo largo de las simulaciones')

    chart = base + ures
    output = (chart & stab_hist(stab)).resolve_scale(x='shared').configure_axis(
                    grid=False
                    )

    if save:
        output.save(f'.\\output\\avg vs avg.svg', scale_factor=2.0)

    if echo:
            return output

# Inter_intra comparison
def intra_inter(dataFrame, stab,  side="S", style='opaque', echo=False, save=False):
    """ Graphs an aggregated style graph showing the average between each simulation

    Arguments:
        dataFrame {Pandas Data Frame} -- The simulation Data Frame
        num {int} -- The number of simulations


    Keyword Arguments:
        side {str} -- Buyer ("B") or Seller ("S") (default: {"S"})
        stryle {str} -- Styler for altair themes

    Returns (if echo):
        output -- Altair **interactive** graph
    """

    # Checks if chromedriver is in directory for saving
    if save and not os.path.isfile('./chromedriver.exe'):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), 
                                'chromedriver.exe')
    
    plot_avg=pd.DataFrame()
    plot_overall=pd.DataFrame()
    ures_df=pd.DataFrame()
    assert (side == "S" or side == "B"), 'Side must be S or B'
    # Gets the number of simulations
    sim_str=dataFrame.columns[-1]
    place=sim_str.find("_")
    sim_num=int(sim_str[:place])
    # Gets the overall average:

    plot_overall['value']=dataFrame.filter(regex=f"{side}_._Precio").mean(axis=1)
    plot_overall.index.names=['time']
    plot_overall=plot_overall.reset_index()
    plot_overall=plot_overall.melt("time")
    plot_overall['tipo'] = 'Media entre'


    # Gets the average in each iteration:
    for i in range(sim_num):
        reg=f"{i}_{side}_._Precio"
        plot_avg[f'Avg {i}']=dataFrame.filter(regex=reg).mean(axis=1)
    plot_avg.index.names=['time']
    plot_avg=plot_avg.reset_index()
    plot_avg=plot_avg.melt("time")
    plot_avg['tipo']=['Media dentro' for x in plot_avg['variable']]


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
        avg=alt.Chart(plot_avg).mark_line(opacity=0.5).encode(
            x="time:Q",
            y=alt.Y('value:Q',
                    scale=alt.Scale(zero=False)),
            detail='variable',
            color=alt.Color('tipo',
                            scale=alt.Scale(
                                domain=['S', 'B', 'Media dentro', 'Media entre'],
                                range=['green', 'red', '#2E578C', '#E7A13D']))
        )

        overall=alt.Chart(plot_overall).mark_line(opacity=1).encode(
            x="time:Q",
            y=alt.Y('value:Q',
                    scale=alt.Scale(zero=False)),
            detail='variable',
            color=alt.Color('tipo',
                            scale=alt.Scale(
                                domain=['S', 'B', 'Media dentro', 'Media entre'],
                                range=['green', 'red', '#2E578C', '#E7A13D']))
        )

        ures=alt.Chart(ures_df).mark_line(opacity=0.3).encode(
            x=alt.X('time:Q', title="Tiempo"),
            y=alt.Y('value:Q', title="Precio Esperado", 
                    scale=alt.Scale(zero=False)),
            detail='variable',
            color=alt.Color('tipo', legend=alt.Legend(title="Indicadores"),
                            scale=alt.Scale(
                                domain=['S', 'B', 'Media dentro', 'Media entre'],
                                range=['green', 'red', '#2E578C', '#E7A13D']))
        ).properties(title='Media de los precios dentro y entre simulaciones para '  
        f' {"Vendedores" if side == "S" else "Compradores"}')
    
    chart = ures + avg + overall
    output = alt.vconcat(chart, stab_hist(stab), spacing=0
                    ).resolve_scale(x='shared'
                    ).configure_axis( grid=False)
    if save:
        output.save(f'.\\output\\Inter-Intra {side}.svg', scale_factor=2.0)

    if echo:
            return output

    