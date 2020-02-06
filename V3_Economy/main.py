import pandas as pd

from agents import Buyer, Seller
from market import Market

"""
TODO:
Known problems / Future improvements:
- Sometimes one agents skips when the last one to exit leaves
- Change graphical interphace to Altair/Seaborn
- Mean function sometimes breaks
"""

listSellers = [Seller(i, 10, 20, tipe="delta") for i in range(3)]
listBuyers = [Buyer(i, 20, 30, tipe="delta") for i in range(4)]
market = Market(listSellers, listBuyers, 50, echo=False)

simulationDf = pd.DataFrame()


#FIXME: This part does not work!!!!
for i in range(5): 
    while not market.checkEndOfTime():
        market.moveTime()

    # For supported styles, plt.style.available
    market.matplotGraph('Solarize_Light2')
    market.dataFrameMaker(i)
    simulationDf = simulationDf.append(market.df, sort=False)

    for seller in listSellers:
        seller.restart()

    for buyer in listBuyers:
        buyer.restart()
    market.restart()

simulationDf


