import random

from buyer import Buyer
from market import Market
from seller import Seller

"""
Known problems / Future improvements:
- Suplementary graphical interface
"""

<<<<<<< HEAD
listSellers = [Seller(i, 0, 10) for i in range(1)]
listBuyers = [Buyer(i, 10, 20) for i in range(2)]
=======
listSellers = [Seller(i, 10, 20, round=2) for i in range(1)]
listBuyers = [Buyer(i, 20, 30, round=2) for i in range(3)]
>>>>>>> 7435af81439e564cf303ce0e4ec2ea357f7762d3

market = Market(listSellers, listBuyers, 50)

while not market.checkEndOfTime():
    market.moveTime()

market.graph()