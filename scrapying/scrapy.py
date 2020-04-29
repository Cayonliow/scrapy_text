import os
import sys
import requests
import re
import zipfile, urllib.request, shutil
from io import StringIO
import io
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from pprint import pprint
from time import sleep
from selenium.webdriver.support.select import Select

TO_PRINT=False
HTML_PARSER = "html.parser"
# ROOT_URL = 'http://data.gcis.nat.gov.tw'

class Scrapy:
    def __init__(self,  url='http://data.gcis.nat.gov.tw/', 
                        sub_url='od/datacategory', 
                        output_path='output/'):
        self.url = url
        self.sub_url = sub_url
        self.output_path = output_path
        self.zip_path = self.output_path + 'zip/'
        self.char_list_path = self.output_path + 'dict/'
        print('     class Scrapy is initialized')

    def get_catagory_link_list(self):
        homepage = self.url + self.sub_url
        list_req = requests.get(homepage)
        if TO_PRINT: print('     REQUESTING to ', homepage)
        catagory_links = []
        if list_req.status_code == requests.codes.ok:
            soup = BeautifulSoup(list_req.content, HTML_PARSER)
            for _ultag in soup.find_all('ul', {'id': 'cate2'}):
                for _litag in _ultag.find_all('li'):
                    for _link in _litag.find_all('a', href=True):
                        if TO_PRINT: print('         Get sublink', _link['href'])
                        catagory_links.append(_link['href'])
        else:
            if TO_PRINT: print('     Access to ',homepage, ' is failed')
        
        return catagory_links

    def access_pages(self, path_links):
        file_links = []
        file_name = []
        
        if TO_PRINT: print('     ACCESSING to subpages')
        # driver = webdriver.Firefox()
        driver = webdriver.Chrome()
        for links in path_links:
            driver.get(self.url + links)
            if TO_PRINT: print('         Access to', self.url + links)
            
            element = driver.find_element_by_class_name('csv')
            element_text = driver.find_element_by_partial_link_text("登記").text
            outer_html=element.get_attribute('outerHTML')

            try:
                found_file_url = re.search('(\'(.+?)\')', outer_html).group(1)

            except AttributeError:
                found_file_url = ''

            found = element_text.replace('(\'(.+?)\')', '')
            file_links.append(found_file_url.replace('\'', ''))#.replace('(', '').replace(')', ''))
            if TO_PRINT: print('             Get file name ', found)
            file_name.append(found.replace('\'', ''))
                
        driver.quit()

        return file_links, file_name

    def get_files(self, files_link, file_name):
        if TO_PRINT: print('     DOWNLOADING file')
        for idx, _file in enumerate(files_link):
            res = requests.get(self.url + _file, stream=True)
            if TO_PRINT: print('         Access to ', self.url, _file)
            with open(self.zip_path + file_name[idx] + '.zip','wb') as f: 
                if TO_PRINT: print('             Save file ', file_name[idx], '.zip')
                f.write(res.content) 
