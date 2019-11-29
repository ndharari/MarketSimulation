import random

from buyer import Buyer
from market import Market
from seller import Seller

"""
Known problems / Future improvements:
- Suplementary graphical interface
"""

listSellers = [Seller(i, 10, 20, round=2) for i in range(1)]
listBuyers = [Buyer(i, 20, 30, round=2) for i in range(3)]


market = Market(listSellers, listBuyers, 50)

while not market.checkEndOfTime():
    market.moveTime()

market.graph()