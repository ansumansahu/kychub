'''
Month_assigned : May
Date Submitted : 04-05-2022
Date_source_name : KERALA  MLAs
Harvesting_URL : https://www.sarkaritel.com/states/mla_list.php?state=KL
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
    url = 'https://www.sarkaritel.com/states/mla_list.php?state=KL'
    driver.get(url)
    time.sleep(1)

    try:
        li = driver.find_elements(By.XPATH, '/html/body/div/div/div[2]/div/div[3]/div/div[2]/div[1]/div/div/div/div/table/tbody/tr')
        for i in range(4, len(li), 2):
            data_dict = {}
            fullName = ''
            title = ''
            politicalPartyName = ''
            constituency = ''

            try:
                temp = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/div[3]/div/div[2]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]').text
                title = temp.split(' ')[0].strip()
                fullName = " ".join(temp.split(' ')[1:])
            except Exception:
                pass

            try:
                constituency = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/div[3]/div/div[2]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[3]').text
            except Exception:
                pass

            try:
                politicalPartyName = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/div[3]/div/div[2]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[4]').text
            except Exception:
                pass

            summary = fullName + ' is a Member of Legislative Assembly of Kerala representing ' + politicalPartyName

            if fullName:
                data_dict['fullName'] = fullName
                data_dict['title'] = title
                data_dict['category'] = 'PEP'
                data_dict['designation'] = 'Member of Legislative Assembly'
                data_dict['politicalPartyName'] = politicalPartyName
                data_dict['constituency'] = constituency
                data_dict['country'] = 'India'
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
