import os
import re
import numpy as np
import pandas as pd

TO_PRINT=False

class CharCollector:
    def __init__(self, file_path):
        self.file_path = file_path
        print('     class CharCollector is initialized')

    def get_file_list(self):
        if TO_PRINT: print('     GETTING input file list')
        if os.path.isdir(self.file_path):
            csv_list = list(filter(lambda x: '.csv' in x,os.listdir(self.file_path)))
        else:
            if TO_PRINT: print('There is no directory named ',self.file_path)
            exit(1)
        
        assert len(csv_list) > 0
        return np.array(csv_list)

    def get_shop_name_from_all_files(self, file_list):
        if TO_PRINT: print('     GETTING shop name from files')
        name_list = []
        not_hans_name_list = []
        for _file in file_list:
            if TO_PRINT: print('         Getting names from file ', _f)
            if os.path.isfile(self.file_path + str(_file)):
                df  = pd.read_csv(self.file_path + str(_file), encoding='utf-8')
                df.columns = [x for x in range(df.shape[1])]
                new_name, new_not_hans_name = self.get_name_list(np.array(df[1]))
                name_list += new_name
                not_hans_name_list += new_not_hans_name

        return np.array(name_list), np.array(not_hans_name_list)

    def get_name_list(self, word_list):
        temp_word_list = []
        temp_not_hans_word_list = []
        for _word in word_list:
            not_hans =  re.compile('[^\u4E00-\u9Fff]')
            res = not_hans.findall(_word)

            if len(res) == 0:
                temp_word_list.append(_word.replace('\ufeff', ''))
            else:
                if TO_PRINT: print('             contains non-hans character: ', _word)
                temp_not_hans_word_list.append(_word)
        return temp_word_list, temp_not_hans_word_list

    def get_hans_char_from_all_words(self, name_list):
        if TO_PRINT: print('         GETTING characters', end='')
        self.char_list = []
        for idx, name in enumerate(name_list):
            if idx % 5000 == 0:
                if TO_PRINT: print(".",end = '',flush = True)
            self.get_char_list(name)
        return np.array(self.char_list)

    def get_char_list(self, word_list):
        for _word in word_list:
            for _char in _word:
                print('.', end='', flush=True)
                if _char not in self.char_list:
                    if '\u4e00' <= _char <= '\u9fff': # detect whether is hans
                        self.char_list.append(_char)
