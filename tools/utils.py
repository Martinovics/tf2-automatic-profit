import os
import json
from tools.config import Config as cfg




def to_keys(scrap: int) -> float:  # not the best, but close enough
    return round(scrap / (cfg.KEY_PRICE * 9), 2)




def name_from_path(path: str) -> str:
    path = path.split('/') if '/' in path else path.split('\\')
    return path[-1]




def read_file(path_to_file: str) -> list:
    if 'pricelist' in path_to_file:
        with open(path_to_file, 'r', encoding='utf-8') as f:
            pricelist = f.read()
        return json.loads(pricelist)
    
    elif 'polldata' in path_to_file:
        with open(path_to_file, 'r', encoding='utf-8') as f:
            polldata = f.read()
        polldata = json.loads(polldata)

        # reduce data size
        if 'offerData' in polldata:
            polldata = polldata['offerData']
        else:
           return []

        polldata_ = []
        for _, trade in polldata.items():
            if 'isAccepted' in trade:
                if trade['isAccepted'] and trade['partner'] not in cfg.ADMINS:
                    polldata_.append(trade)
        return polldata_

    else:
        return []


