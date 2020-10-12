from typing import List




class Config:
    KEY_PRICE: float = 45

    ADMINS: List[str] = []
    PATHS: List[str] = []  # like "C:/tf2autobot-master/files/botusername" or like "/home/tf2autobot-master/files/botusername"

    MOST_PRIFIT_ITEMS_COUNT: int = 5   # print x amount of the most profitable items
    LEAST_PRIFIT_ITEMS_COUNT: int = 5  # print x amount of the least profitable items
    '''
    MOST_PRIFIT_ITEMS_72H: int = 5     # print x amount of the most profitable items over 72H
    MOST_TRADED_ITEMS_COUNT: int = 5   # print x amount of the most traded items
    LEAST_TRADED_ITEMS_COUNT: int = 5  # print x amount of the least traded items
    '''

    PRINT_ALL_TRADES: bool = False




class Const:
    CURRENCIES: dict = {'5021;6': Config.KEY_PRICE * 9, '5002;6': 9, '5001;6': 3, '5000;6': 1}  # key, ref, rec, scrap
