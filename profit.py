import os
import re
import json
from datetime import datetime
from config import config as cfg




def to_keys(total_scrap: int) -> float:
    return round(total_scrap / (cfg['key_price'] * 9), 2)




for path in cfg['files_path']:
    account_name = path.split('/')[-1] if '/' in path else path.split('\\')[-1]
    print(f"\nProfits for {account_name} --{'--=-=-==-==-===-==-==-=-=--' * 3}--\n")


    # load pricelist and polldata json files -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    with open(os.path.join(path, 'pricelist.json'), 'r', encoding='utf-8') as f:
        pricelist = f.read()
    pricelist = json.loads(pricelist)


    with open(os.path.join(path, 'polldata.json'), 'r', encoding='utf-8') as f:
        polldata = f.read()
    polldata = json.loads(polldata)

    if 'offerData' in polldata:
        polldata = polldata['offerData']
    else:
        print(f"{account_name} haven't made any trades yet.")
        continue

    polldata_ = []
    for _, trade in polldata.items():
        if 'isAccepted' in trade:
            if trade['isAccepted'] and trade['partner'] not in cfg['admins']:
                polldata_.append(trade)
    polldata = polldata_



    # get (only) accepted trades -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    first_trade_time = datetime.now()

    item_data = {}
    currencies = ['5021;6', '5002;6', '5001;6', '5000;6']  # key, ref, rec, scrap

    for trade in polldata:

        trade_time = datetime.fromtimestamp(trade['finishTimestamp'] // 1000)
        if trade_time < first_trade_time:
            first_trade_time = trade_time


        rate = trade['value']['rate'] * 9  # key price in scrap (at that time)

        our_currencies = 0
        if '5021;6' in trade['dict']['our']:  # key
            our_currencies += trade['dict']['our']['5021;6'] * rate
        if '5002;6' in trade['dict']['our']:  # ref
            our_currencies += trade['dict']['our']['5002;6'] * 9
        if '5001;6' in trade['dict']['our']:  # rec
            our_currencies += trade['dict']['our']['5001;6'] * 3
        if '5000;6' in trade['dict']['our']:  # scrap
            our_currencies += trade['dict']['our']['5000;6'] * 1

        their_currencies = 0
        if '5021;6' in trade['dict']['their']:  # key
            their_currencies += trade['dict']['their']['5021;6'] * rate
        if '5002;6' in trade['dict']['their']:  # ref
            their_currencies += trade['dict']['their']['5002;6'] * 9
        if '5001;6' in trade['dict']['their']:  # rec
            their_currencies += trade['dict']['their']['5001;6'] * 3
        if '5000;6' in trade['dict']['their']:  # scrap
            their_currencies += trade['dict']['their']['5000;6'] * 1


        action = 'sold' if [sku for sku in trade['dict']['our'] if sku not in currencies] else 'bought'

        if action == 'sold':
            sku = [sku for sku in trade['dict']['our'] if sku not in currencies]
        else:
            sku = [sku for sku in trade['dict']['their'] if sku not in currencies]

        if sku:
            sku = sku[0]  # multiple items
        else:
            continue


        date = datetime.fromtimestamp(trade['finishTimestamp'] // 1000).strftime('%d-%m-%y_%H:%M:%S')
        sold = {'action': 'sold', 'price': their_currencies - our_currencies, 'date': date}
        bought = {'action': 'bought', 'price': our_currencies - their_currencies, 'date': date}
        if sku not in item_data:
            item_data[sku] = {'profit': 0, 'trades': []}

        item_data[sku]['trades'].append(sold) if action == 'sold' else item_data[sku]['trades'].append(bought)


    item_data = dict(sorted(item_data.items()))



    date_profits = {}
    for sku, data in item_data.items():
        profit = 0  # profit on this item

        sold = len([trade for trade in data['trades'] if trade['action'] == 'sold'])
        bought = len([trade for trade in data['trades'] if trade['action'] == 'bought'])

        len_pairs = min([sold, bought])  # the number of bought-sold pairs

        c = c_ = 0
        date = '01-01-1999'  # no date
        sold = sold_price = sold_total = 0
        bought = bought_price = bought_total = 0
        for trade in data['trades']:
            c_ = c

            if sold < len_pairs and trade['action'] == 'sold':
                sold_total += trade['price']
                sold_price = trade['price']
                sold += 1
                c += 1

                date = datetime.strptime(trade['date'], '%d-%m-%y_%H:%M:%S')
                date = datetime.strftime(date, '%d-%m-%Y')

            elif bought < len_pairs and trade['action'] == 'bought':
                bought_total += trade['price']
                bought_price = trade['price']
                bought += 1
                c += 1

            if bought == sold and (0 < bought and 0 < sold) and c_ < c:
                if date in date_profits:
                    date_profits[date] += (sold_price - bought_price)
                else:
                    date_profits[date] = (sold_price - bought_price)

        item_data[sku]['profit'] = sold_total - bought_total



    # print item data -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    max_len_sku = max([len(sku) for sku in item_data])
    max_len_profit = max([len(f"{to_keys(item_data[sku]['profit'])} keys") for sku in item_data])
    if cfg['print_item_data']:
        for sku, data in item_data.items():
            profit = to_keys(data['profit'])
            trades = [f"{trade['action'][0]}{to_keys(trade['price'])}k{re.sub(r'[-:]', '', trade['date'])}"
                      for trade in data['trades']]

            tab1 = (max_len_sku + 2 - len(sku)) * ' '
            tab2 = (max_len_profit + 3 - len(f"{profit} keys")) * ' '

            print(f"{sku}{tab1}profit: {profit} keys{tab2}trades: {'  '.join(trades)}")
        print()



    # get daily profit -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    dates = list(date_profits.keys())
    dates.sort(key=lambda date_: datetime.strptime(date_, '%d-%m-%Y'))  # sort dates
    date_profits = {key: date_profits[key] for key in dates}

    print(f"Day by day profit: (total: ~{round(sum([to_keys(date_profits[date]) for date in date_profits]), 2)} keys)")

    c = 1
    for date, profit in date_profits.items():
        print(f'{c}.' + '\t' + f"{date}  {to_keys(profit)} keys")
        c += 1
    print()



    # get most and least profitable items -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    item_profits = []
    for sku, data in item_data.items():
        item_profits.append({'sku': sku, 'profit': data['profit']})
    item_profits = sorted(item_profits, key=lambda k: k['profit'], reverse=True)


    s = ''
    for item in item_profits:
        sku = item['sku']
        item_profit = to_keys(item['profit'])

        s += f"{sku}{(max_len_sku + 2 - len(sku)) * ' '}{item_profit} keys\n"
        if s.count('\n') == cfg['most_profit_items_count']:
            break
    print(f"The most profitable items:\n{s}")


    s = ''
    for item in reversed(item_profits):
        sku = item['sku']
        item_profit = to_keys(item['profit'])

        s += f"{sku}{(max_len_sku + 2 - len(sku)) * ' '}{item_profit} keys\n"
        if s.count('\n') == cfg['least_profit_items_count']:
            break
    print(f"The least profitable items:\n{s}")



    # estimated profits -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    profit = sum([item_data[sku]['profit'] for sku in item_data])

    days = (datetime.now() - first_trade_time).days
    s_time = f" in {days} (full)days, that's {to_keys(profit/days)} keys / 24h"

    print(f"estimated profit: {to_keys(profit)} keys{s_time}")


    profit = 0
    for sku, data in item_data.items():
        if 0 < len(data['trades']):

            trade = data['trades'][-1]
            if trade['action'] == 'bought':

                for listing in pricelist:
                    if listing['sku'] == sku:
                        profit += ((listing['sell']['keys'] * cfg['key_price'] * 9) + (listing['sell']['metal'] * 9)) - trade['price']
                        break

    print(f"potential profit: {to_keys(profit)} keys")
