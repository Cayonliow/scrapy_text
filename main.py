import os 
import numpy as np

from parameter import *
from pprint import pprint

def main():
    print('EXECUTING MAIN.PY: COMBINING DICTIONARY')
    dictionary = []
    dcit_file = [DICT_FSW, DICT_SCR]

    for _df in dcit_file:
        print('     Loading character list', end='', flush=True)
        with open(_df, 'r') as filehandle:
            for idx, _line in enumerate(filehandle):
                if idx% 1000 ==0:
                    print('.', end='', flush=True)
                _char = _line.strip()
                if _char not in dictionary:
                    dictionary.append(_line.strip())
        print('')
    
    dictionary = np.array(dictionary)
    print('The shape of dictionary ', dictionary.shape, '\n')

    if os.path.isdir(OUTPUT_PATH) == False:
        os.mkdir(OUTPUT_PATH)
        if os .path.isdir(FINAL_DICT_PATH) == False:
            os .mkdir(FINAL_DICT_PATH)
    
    with open(FINAL_DICT_PATH + 'dictionary.txt', 'w') as filehandle:  
        for _char in dictionary:
            filehandle.write(_char+'\n')

    shop_name = []
    with open(SHOP_NAME_LIST_SCR, 'r') as filehandle:
            print('     Loading shop name list', end='', flush=True)
            for idx, _line in enumerate(filehandle):
                if idx% 5000 ==0:
                    print('.', end='', flush=True)
                name = _line.replace('有限公司', '').replace('股份', '')
                # too slow
                # if name not in shop_name:
                #     shop_name.append(name)
                shop_name.append(name)

    shop_name = np.array(shop_name)
    print('\nThe shape of shop name list ', shop_name.shape, '\n')

    with open(FINAL_DICT_PATH + 'shop_name.txt', 'w') as filehandle:  
        for _name in shop_name:
            filehandle.write(_name)

if __name__ == '__main__':
    main()
