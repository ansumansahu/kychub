'''
Month_assigned : April
Date Submitted : 26-04-2022
Date_source_name : Jonesboro Daily Police Report
Harvesting_URL : https://drive.google.com/drive/folders/1B8KCthkls82MS8CppQ8iWo6pty9JJ8g-
Data_Extractor : Ansuman Sahu
'''

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

import pdftables_api
import xlrd

def to_json(data_list):
    hash_obj = json.dumps(data_list)
    with open('json/dictionary.json', 'w') as ts:
        ts.write(hash_obj)


def get_hash_of_html(html_string):
    hash_object = hashlib.md5(html_string.encode('utf-8'))
    hash_of_html = hash_object.hexdigest()
    return hash_of_html


def get_data(slug_name):
    last_updated_dev = int(time.time())
    update_label_ts = int(time.time())

    data_list=[]
    path = r"2022_April Reports.xlsx"
    # To open Workbook
    wb = xlrd.open_workbook(path)
    l = len(wb.sheet_names())

    for k in range(l):
        sheet = wb.sheet_by_index(k)
        rows = sheet.nrows
        cols = sheet.ncols

        for i in range(rows):
            x = sheet.row_values(i)
            fullName = x[7]
            if fullName:
                data_dict = {}
                data_dict['fullName'] = fullName
                data_dict['category'] = 'CRIME'
                data_dict['dateOfIncident'] = 'April 2022'
                data_dict['crimeLocation'] = x[4]
                data_dict['crimeDescription'] = x[5]
                data_dict['additionalInfo'] = "Incident Number: " + str(x[0]) + " ,Reporting Officer: " + str(x[3]) + " ,MO: " + str(x[6])
                data_dict['summary'] = fullName + " is a individual reported by Jonesboro Police Department, Arkansas, U.S"
                # print(data_dict)
                html_hash = get_hash_of_html(str(data_dict))
                data_dict['UpdationFlag'] = True
                data_dict['RawHtml'] = html_hash
                data_dict['LastUpdatedDev'] = last_updated_dev
                data_dict['UpdateLabelTs'] = update_label_ts

                if data_dict:
                    data_list.append(data_dict)

    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    # print(data_list)
