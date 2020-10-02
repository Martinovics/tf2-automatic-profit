from typing import List




class Config:
    KEY_PRICE: float = 45

    ADMINS: List[str] = []
    PATHS: List[str] = []

    MOST_PRIFIT_ITEMS_COUNT = 5   # print x amount of the most profitable items
    LEAST_PRIFIT_ITEMS_COUNT = 5  # print x amount of the least profitable items
    MOST_TRADED_ITEMS_COUNT = 5   # print x amount of the most traded items
    LEAST_PRIFIT_ITEMS_COUNT = 5  # print x amount of the least traded items

    PRINT_ALL_TRADES: bool = False




class Const:
    CURRENCIES: List[str] = ['5021;6', '5002;6', '5001;6', '5000;6']  # key, ref, rec, scrap
