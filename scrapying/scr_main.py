#!/bin/sh
import os
import sys
import subprocess
import requests
import re
import zipfile, urllib.request, shutil
import io
from io import StringIO
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from pprint import pprint
from time import sleep
from selenium.webdriver.support.select import Select
from argparse import ArgumentParser
from distutils.util import strtobool

from charcollector import CharCollector
from scrapy import Scrapy
from parameter import *

TO_PRINT=False

HTML_PARSER = "html.parser"
ROOT_URL = 'http://data.gcis.nat.gov.tw'
LIST_URL = '/od/datacategory'

def main():
    print('EXECUTING SCR_MAIN.PY')
    scrapy_site = Scrapy(url=ROOT_URL, sub_url=LIST_URL, output_path=OUTPUT_PATH)
    catagory_links = scrapy_site.get_catagory_link_list()
    file_links, file_names = scrapy_site.access_pages(catagory_links)
    scrapy_site.get_files(file_links, file_names)

    with open(ZIP_FILE, 'w') as fr:
        for _index, _file in enumerate(os.listdir(ZIP_PATH)):
            if _file.endswith('.zip'):

                ori_name = (ZIP_PATH + _file)
                fr.writelines(_file + '\n')

                zf = zipfile.ZipFile(ori_name)

                zipfile_member = []
                for _member in zf.namelist():
                    if _member.endswith('.csv'):
                        zipfile_member.append(_member)

                for _member in zipfile_member:
                    try:
                        zf.extract(_member, path=UNZIP_PATH, pwd=None)
                        fr.writelines('      |-- ' + _member + '\n')
                        
                    except zipfile.BadZipfile:
                        fr.writelines('      |-- (BadZipFile)' + _member + '\n')
                        subprocess.call('mv ' + ori_name.replace(' ', '\ ').replace('(','\(').replace(')','\)') + ' ' + BADFILE_PATH, shell=True)
                        print('BAD ZIP FILE: ', _member, 'is found from ' + ori_name + ' and it is moved into ', BADFILE_PATH)
                
            
    char_collect = CharCollector(file_path = UNZIP_PATH)
    file_list = char_collect.get_file_list()
    name_list, invalid_name_list = char_collect.get_shop_name_from_all_files(file_list)
    char_list = char_collect.get_hans_char_from_all_words(name_list)

    with open(RESULT_PATH + 'char_list.txt', 'w') as filehandle:
        for char in char_list:
            filehandle.write('%s\n' % char)

    with open(RESULT_PATH + 'name_list.txt', 'w') as filehandle:
        for name in name_list:
            filehandle.write(name+'\n')


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument("-p",
                        "--print",
                        help="whether to print out the details",
                        dest="toprint")

    args = parser.parse_args()
    TO_PRINT = strtobool(args.toprint)

    main()
