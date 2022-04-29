'''
Month_assigned : April
Date Submitted : 29-04-2022
Date_source_name : monroe county inmates info
Harvesting_URL : https://www.keysso.net/jailog
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

    PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver\\chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(PATH)
    driver.maximize_window()

    data_list = []
    url = 'https://www.keysso.net/jailog'
    driver.get(url)
    time.sleep(1)

    try:
        li = driver.find_elements(By.XPATH, '/html/body/main/div[2]/div')
        for i in range(2, len(li)+1):
            data_dict = {}
            fullName = ''
            dob = ''
            age = ''
            charges = ''
            additionalInfo = ''

            try:
                fMN = driver.find_element(By.XPATH, f'/html/body/main/div[2]/div[{i}]/div[1]/div[1]/div/strong').text.strip()
                lN = driver.find_element(By.XPATH, f'/html/body/main/div[2]/div[{i}]/div[1]/strong').text.strip()
                fullName = fMN + " " + lN
            except Exception:
                pass

            try:
                additionalInfo = "ID: " + driver.find_element(By.XPATH, f'/html/body/main/div[2]/div[{i}]/div[1]/div[2]/div').text.strip()
            except Exception:
                pass

            try:
                dob = driver.find_element(By.XPATH, f'/html/body/main/div[2]/div[{i}]/div[2]').text.strip()
            except Exception:
                pass

            try:
                age = driver.find_element(By.XPATH, f'/html/body/main/div[2]/div[{i}]/div[3]').text.strip()
            except Exception:
                pass

            try:
                additionalInfo += "; Location: " + driver.find_element(By.XPATH, f'/html/body/main/div[2]/div[{i}]/div[4]').text.strip()
            except Exception:
                pass

            try:
                charges = driver.find_element(By.XPATH, f'/html/body/main/div[2]/div[{i}]/div[5]').text.replace('\n', ',').strip()
            except Exception:
                pass

            try:
                additionalInfo += "; Bond-Case & Arraignment Date: " + driver.find_element(By.XPATH, f'/html/body/main/div[2]/div[{i}]/div[6]').text.replace('\n', ',').strip()
            except Exception:
                pass

            summary = fullName + ' is a current inmate listed in the jail records of Monroe County'

            if fullName:
                data_dict['fullName'] = fullName
                data_dict['age'] = age
                data_dict['dob'] = dob
                data_dict['category'] = 'CRIME'
                data_dict['charges'] = charges
                data_dict['additionalInfo'] = additionalInfo
                data_dict['summary'] = summary
                # print(data_dict)
                html_hash = get_hash_of_html(str(data_dict))
                data_dict['UpdationFlag'] = True
                data_dict['RawHtml'] = html_hash
                data_dict['LastUpdatedDev'] = last_updated_dev
                data_dict['UpdateLabelTs'] = update_label_ts

            if data_dict:
                data_list.append(data_dict)

    except Exception:
        pass

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    # print(data_list)
