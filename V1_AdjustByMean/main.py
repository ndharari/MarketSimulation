import random

from buyer import Buyer
from market import Market
from seller import Seller

"""
Known problems / Future improvements:
- Better the ajust mechanism
- End game at market equilibrium, not at set number of turns ~~tricky~~
- Better the graphical interface
"""

listSellers = [Seller(i, 0, 20) for i in range(5)]
listBuyers = [Buyer(i, 20, 40) for i in range(5)]

market = Market(listSellers, listBuyers, 15)

while not market.checkEndOfTime():
    market.moveTime()

market.graph()
