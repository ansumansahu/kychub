'''
Month_assigned : April
Date Submitted : 22-04-2022
Date_source_name : jefferson county sheriffs office outstanding warrants
Harvesting_URL : https://files4.1.revize.com/jeffersoncountynew/Sheriff/Most%20wanted/outstanding%20warrant%20listing-public.pdf
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
    # Uncomment to convert pdf to xlsx
    # # API KEY VERIFICATION
    # conversion = pdftables_api.Client('e5gso7sbpd6r')
    # # PDf to Excel
    # conversion.xlsx("C:/Users/Ansh/Downloads/outstanding warrant listing-public.pdf", "outstanding warrant listing-public")

    path = r"outstanding warrant listing-public.xlsx"
    # To open Workbook
    wb = xlrd.open_workbook(path)
    l = len(wb.sheet_names())

    for k in range(l):
        sheet = wb.sheet_by_index(k)
        rows = sheet.nrows
        cols = sheet.ncols
        v1, v2, v3 = 0, 0, 0

        for i in range(rows):
            x = sheet.row_values(i)
            data_dict = {}
            temp = ''
            fullName = ''
            age = ''
            city = ''
            state = ''
            warrantType = ''

            if x[0] == 'Warrant #':
                le = len(x)
                for key in range(le):
                    if x[key] == 'Warrant Type':
                        v1 = key
                    if x[key] == 'Street':
                        v2 = key
                    if x[key] == 'City':
                        v3 = key

            if x[0] and x[0] != 'Warrant #':
                try:
                    fullName = x[v1 + 3]
                except Exception:
                    pass

                try:
                    warrantType = x[v1]
                except Exception:
                    pass

                v4 = v1
                v6 = 0
                while v6 != v4:
                    temp += str(x[v6])
                    v6 += 1
                additionalInfo = "Warrant: " + temp + " ,Bond Amount: " + str(x[v1 + 1])
                additionalInfo += " ,Bond Remark: " + x[v1 + 2]

                try:
                    age = int(x[v1 + 4])
                except Exception:
                    pass

                v5 = v3 - v2
                fullAddress = ''
                while v5:
                    fullAddress += str(x[v3 - v5]) + " "
                    v5 -= 1
                try:
                    city = x[v3]
                except Exception:
                    pass

                try:
                    state = x[v3 + 1]
                except Exception:
                    pass

                if fullName:
                    data_dict['fullName'] = fullName
                    data_dict['age'] = age
                    data_dict['fullAddress'] = fullAddress
                    data_dict['city'] = city
                    data_dict['state'] = state
                    data_dict['warrantType'] = warrantType
                    data_dict['additionalInfo'] = additionalInfo
                    data_dict['category'] = 'CRIME'
                    data_dict['summary'] = fullName + ' is an individual present in warrant list as published by Jefferson County, Colorado, U.S'
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
    print(data_list)
