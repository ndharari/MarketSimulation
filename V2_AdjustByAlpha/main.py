from buyer import Buyer
from market import Market
from seller import Seller

"""
Known problems / Future improvements:
- Sometimes one agents skips when the last one to exit leaves
- Change graphical interphace to Altair/Seaborn
"""

listSellers = [Seller(i, 10, 20, tipe="delta") for i in range(3)]
listBuyers = [Buyer(i, 20, 30, tipe="delta") for i in range(3)]


market = Market(listSellers, listBuyers, 50, echo=False)

while not market.checkEndOfTime():
    market.moveTime()

market.matplotGraph('Solarize_Light2')  # For supported styles, plt.style.available

# market.dataFrameMaker()
# market.getDataFrame()

