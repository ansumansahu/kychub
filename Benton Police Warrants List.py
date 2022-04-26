'''
Month_assigned : April
Date Submitted : 26-04-2022
Date_source_name : Benton Police Warrants List
Harvesting_URL : https://bentonpolice.org/divisions/cid/warrants
Data_Extractor : Ansuman Sahu
'''

import re
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
# from ..general_utility import get_hash_of_html
# from ..s3_upload import hash_check
import hashlib
import json
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as bs
import time
import requests

# import necessary classes
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def to_json(data_list):
    hash_obj = json.dumps(data_list)
    with open('json/dictionary.json', 'w') as ts:
        ts.write(hash_obj)


def get_hash_of_html(html_string):
    hash_object = hashlib.md5(html_string.encode('utf-8'))
    hash_of_html = hash_object.hexdigest()
    return hash_of_html


def get_soup(url):
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')
    return soup


def get_data(slug_name):
    last_updated_dev = int(time.time())
    update_label_ts = int(time.time())

    data_list = []

    url = 'https://bentonpolice.org/divisions/cid/warrants'
    soup = get_soup(url)

    data_secs = soup.find('table')
    rows = data_secs.find_all('tr')
    for line in rows:
        data_dict = {}

        temp = line.text
        temp1 = temp.split('Date:')
        importantDates = "Warrant Date: " + temp1[1].strip()
        temp2 = (temp1[0]).split('Warrant #:')
        arrestWarrant = temp2[1].strip()
        temp3 = (temp2[0]).split('Age:')
        age = temp3[1].strip()
        temp4 = (temp3[0]).split('Name:')
        fullName = temp4[1].strip()

        if fullName:
            data_dict['fullName'] = fullName
            data_dict['age'] = age
            data_dict['category'] = 'CRIME'
            data_dict['arrestWarrant'] = arrestWarrant
            data_dict['importantDates'] = importantDates
            data_dict['summary'] = "Benton County Police Department, Washington, U.S has issued an warrant for " + fullName + " dated " + temp1[1].strip()
            # print(data_dict)
            data_dict['UpdationFlag'] = True
            html_hash = get_hash_of_html(str(data_dict))
            data_dict['RawHtml'] = html_hash
            data_dict['LastUpdatedDev'] = last_updated_dev
            data_dict['UpdateLabelTs'] = update_label_ts

        if data_dict:
            data_list.append(data_dict)

    return data_list


if __name__ == "__main__":
    data_list = get_data('slug')
    # to_json(data_list)
    # print(data_list)
