from buyer import Buyer
from market import Market
from seller import Seller

"""
Known problems / Future improvements:
- Suplementary graphical interface
"""

listSellers = [Seller(i, 10, 20, tipe="delta") for i in range(3)]
listBuyers = [Buyer(i, 20, 30, tipe="delta") for i in range(4)]


market = Market(listSellers, listBuyers, 75)

while not market.checkEndOfTime():
    market.moveTime()

market.graph()
