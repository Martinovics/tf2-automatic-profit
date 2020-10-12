import os
import json
from typing import Any
from tools.config import Config as cfg




def to_keys(scrap: int) -> float:  # not the best, but close enough
    return round(scrap / (cfg.KEY_PRICE * 9), 2)




def space(max_length: int, extra_space: int, current_string: str):
    return (max_length + extra_space - len(current_string)) * ' '




def name_from_path(path: str) -> str:
    path = path.split('/') if '/' in path else path.split('\\')
    return path[-1]




def read_file(path: str) -> list:
    
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    
        if path.endswith('polldata.json'):
            data = json.loads(data)

            # reduce data size
            if 'offerData' in data:
                data = data['offerData']
            else:
                return []

            polldata = []
            for _, trade in data.items():
                if 'isAccepted' in trade:
                    if trade['isAccepted'] and trade['partner'] not in cfg.ADMINS:
                        polldata.append(trade)
            return polldata
        
        elif path.endswith('.json'):
            return json.loads(data)
        
        else:
            return data




def write_file(path: str, data: Any) -> None:

    with open(path, mode='w', encoding='utf-8') as f:

        if path.endswith('.json'):
            f.write(json.dumps(data, indent=4, ensure_ascii=False))

        else:
            f.write(str(data))
