config = {
    'key_price': 55,  # actual key price in ref (float)

    # the bot's admins (list of strings); if you don't set all admins it will crash :/
    'admins': ['steamID64', 'steamID64'],

    # the directory's path, which has polldata.json and pricelist.json in it
    'files_path': ['/home/user/on_linux/tf2-automatic-master/files/account_named_directory',
                   'C:\\Users\\user\\on_windows\\tf2-automatic-master\\files\\account_named_directory'],

    'most_profit_items_count': 5,  # print x of the most profitable items
    'least_profit_items_count': 5,    # print x of the least profitable items

    # b1.76k240620_232009 > b 1.76k 24/06/20 23:20:09 >>> bought for 1.76 keys at 23:20:09 on 24th June(06) 2020
    # s1.78k250620_104324 > s 1.78k 25/06/20 10:43:24 >>> sold for 1.78 keys at 10:43:24 on 25th June(06) 2020
    'print_item_data': False  # set this to True to print some info of the items
}
