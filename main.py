import random

from buyer import Buyer
from market import Market
from seller import Seller

"""
Known problems / Future improvements:
- Needs to figure out what happens if sellers>buyers
- Differences in market compositions should be seen
- Better the ajust mechanism
- End game at market equilibrium, not at set number of turns
- Add some Graphical interface to analyse results
"""

listSellers = [Seller(i, 0, 20) for i in range(5)]
listBuyers = [Buyer(i, 20, 40) for i in range(5)]

market = Market(listSellers, listBuyers, 50)

while not market.checkEndOfTime():
    market.moveTime()
