import os
import re
import json
import tools.utils as utils
from datetime import datetime
from tools.config import Config as cfg
from tools.config import Const as const





for path in cfg.PATHS:
    account_name = utils.name_from_path(path)
    print(f"\n\nProfits for {account_name} --{'--=-=-==-====-==-=-=--' * 3}--\n")



    pricelist = utils.read_file(os.path.join(path, 'pricelist.json'))
    polldata = utils.read_file(os.path.join(path, 'polldata.json'))  # accepted, non-admin trades only

    if not polldata:
        print(f"{account_name} haven't made any trades yet.")
        continue



    item_data = {}
    first_trade_time = datetime.now()

    for trade in polldata:

        trade_time = datetime.fromtimestamp(trade['finishTimestamp'] // 1000)
        if trade_time < first_trade_time:
            first_trade_time = trade_time


        # get pures on both sides (in scrap)
        our_curr = their_curr = 0
        for curr, scrap in const.CURRENCIES.items():
            if curr == list(const.CURRENCIES.keys())[0]:
                scrap = trade['value']['rate'] * 9
            
            if curr in trade['dict']['our']:
                our_curr += trade['dict']['our'][curr] * scrap
            if curr in trade['dict']['their']:
                their_curr += trade['dict']['their'][curr] * scrap


        # should think more about this ˇ
        skus = []
        sold_skus = [sku for sku in trade['dict']['our'] if sku not in const.CURRENCIES]
        bought_skus = [sku for sku in trade['dict']['their'] if sku not in const.CURRENCIES]

        action = 'sold' if sold_skus else 'bought'

        if len(sold_skus) != len(bought_skus):
            skus = sold_skus if action == 'sold' else bought_skus

            if skus:
                sku = skus[0]  # multiple items
            else:
                continue
        else:
            continue
        # should think more about this ^


        trade_time = datetime.fromtimestamp(trade['finishTimestamp'] // 1000)
        if trade_time < first_trade_time:
            first_trade_time = trade_time
        trade_time = trade_time#.strftime('%d-%m-%y_%H:%M:%S')

        if sku not in item_data:
            item_data[sku] = {'profit': 0, 'trades': []}

        if action == 'sold':
            item_data[sku]['trades'].append({'action': 'sold', 'price': their_curr - our_curr, 'time': trade_time})
        else:
            item_data[sku]['trades'].append({'action': 'bought', 'price': our_curr - their_curr, 'time': trade_time})



    item_data = dict(sorted(item_data.items()))



    date_profits = {}
    for sku, data in item_data.items():

        trades = data['trades']

        trades_ = []
        s_trades = [trade for trade in trades if trade['action'] == 'sold']
        b_trades = [trade for trade in trades if trade['action'] == 'bought']

        for b in b_trades:
            for s in s_trades:
                
                if b['time'] <= s['time']:
                    trades_.append((b, s))
                    s_trades.remove(s)
                    break
        
        trades = trades_


        s_total = b_total = 0
        for b, s in trades:

            s_total += s['price']
            b_total += b['price']

            # date = datetime.strftime(datetime.strptime(s['time'].strftime('%d-%m-%y_%H:%M:%S'), '%d-%m-%y_%H:%M:%S'), '%d-%m-%Y')
            date = datetime.strftime(s['time'], '%d-%m-%Y')
            if date in date_profits:
                date_profits[date] += (s['price'] - b['price'])
            else:
                date_profits[date] = (s['price'] - b['price'])

        item_data[sku]['profit'] = s_total - b_total



    # print item data -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    max_len_sku = max([len(sku) for sku in item_data])
    max_len_profit = max([len(f"{utils.to_keys(item_data[sku]['profit'])} keys") for sku in item_data])
    if cfg.PRINT_ALL_TRADES:
        for sku, data in item_data.items():
            profit = utils.to_keys(data['profit'])
            trades = [f"{trade['action'][0]}{utils.to_keys(trade['price'])}k{re.sub(r'[-:]', '', trade['time'])}"
                      for trade in data['trades']]

            tab1 = (max_len_sku + 2 - len(sku)) * ' '
            tab2 = (max_len_profit + 3 - len(f"{profit} keys")) * ' '

            print(f"{sku}{tab1}profit: {profit} keys{tab2}trades: {'  '.join(trades)}")
        print()



    # get daily profit -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    dates = list(date_profits.keys())
    dates.sort(key=lambda date_: datetime.strptime(date_, '%d-%m-%Y'))  # sort dates
    date_profits = {key: date_profits[key] for key in dates}

    print(f"Day by day profit: (total: ~{round(sum([utils.to_keys(date_profits[date]) for date in date_profits]), 2)} keys)")

    c = 1
    for date, profit in date_profits.items():
        print(f'{c}.' + '\t' + f"{date}  {utils.to_keys(profit)} keys")
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
        item_profit = utils.to_keys(item['profit'])

        s += f"{sku}{(max_len_sku + 2 - len(sku)) * ' '}{item_profit} keys\n"
        if s.count('\n') == cfg.MOST_PRIFIT_ITEMS_COUNT:
            break
    print(f"The most profitable items:\n{s}")


    s = ''
    for item in reversed(item_profits):
        sku = item['sku']
        item_profit = utils.to_keys(item['profit'])

        s += f"{sku}{(max_len_sku + 2 - len(sku)) * ' '}{item_profit} keys\n"
        if s.count('\n') == cfg.LEAST_PRIFIT_ITEMS_COUNT:
            break
    print(f"The least profitable items:\n{s}")



    # estimated profits -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    profit = total_profit = sum([item_data[sku]['profit'] for sku in item_data])  # total profit; total_profit: save profit value for later use

    days = (datetime.now() - first_trade_time).days
    s_time = f" in {days} (full)days, that's {utils.to_keys(profit/days)} keys / 24h"

    print(f"estimated profit: {utils.to_keys(profit)} keys{s_time}")


    profit = 0  # this isn't accurate, but it can give a rough estimate
    for sku, data in item_data.items():

        c = 0
        trades = data['trades']
        for trade in reversed(trades):
            if trade['action'] == 'bought':
                c += 1
            else:
                break
        trades = trades[len(trades) - c:]  # last 'bought' trades only


        if trades:
            for listing in pricelist:
                if listing['sku'] == sku and listing['enabled']:
                    key = listing['sell']['keys'] * cfg.KEY_PRICE * 9
                    ref = listing['sell']['metal'] * 9

                    for trade in trades:
                        profit += ((key + ref) - trade['price'])

                    break

    print(f"potential profit: {utils.to_keys(profit)} keys")



    # profit since last checked -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    if 'history.json' not in os.listdir('./'):
        with open('./history.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps({}, indent=4, ensure_ascii=False))

    with open('./history.json', 'r', encoding='utf-8') as f:
        history = f.read()
    history = json.loads(history)


    if account_name not in history:
        history[account_name] = {}
    history[account_name][datetime.now().strftime('%d-%m-%Y_%H:%M:%S')] = utils.to_keys(total_profit)


    if 2 <= len(history[account_name]):
        h = history[account_name]
        dates = list(history[account_name].keys())

        print(f"profit since last checked ({dates[-2]}): {round(h[dates[-1]] - h[dates[-2]], 2)} keys")


    with open('./history.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(history, indent=4, ensure_ascii=False))
