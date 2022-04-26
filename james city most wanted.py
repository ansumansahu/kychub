'''
Month_assigned : April
Date Submitted : 26-04-2022
Date_source_name : james city most wanted
Harvesting_URL : https://p2c.jamescitycountyva.gov/wantedlist.aspx
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
    url = 'https://p2c.jamescitycountyva.gov/wantedlist.aspx'
    driver.get(url)
    time.sleep(1)

    try:
        driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/div[2]/div[2]/div[2]/div[5]/div/table/tbody/tr/td[2]/table/tbody/tr/td[5]/select').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/div[2]/div[2]/div[2]/div[5]/div/table/tbody/tr/td[2]/table/tbody/tr/td[5]/select/option[5]').click()
        time.sleep(3)

        li = driver.find_elements(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/div[2]/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr')
        # print(len(li))
        for i in range(1, len(li)+1):
            data_dict = {}
            fullName = ''
            gender = ''
            charges = ''
            additionalInfo = ''
            policeStation = ''

            try:
                temp = driver.find_element(By.XPATH, f'/html/body/form/table/tbody/tr[2]/td/div[2]/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[{i}]/td[1]').text
                temp2 = temp.split('(')
                fullName = temp2[0].strip()
                gender = (temp2[1]).split('/')[1].strip()
            except Exception:
                pass

            try:
                charges = driver.find_element(By.XPATH, f'/html/body/form/table/tbody/tr[2]/td/div[2]/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[{i}]/td[8]').text.strip()
            except Exception:
                pass

            try:
                additionalInfo = "Paper Type: " + driver.find_element(By.XPATH, f'/html/body/form/table/tbody/tr[2]/td/div[2]/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[{i}]/td[9]').text.strip()
            except Exception:
                pass

            try:
                policeStation = driver.find_element(By.XPATH, f'/html/body/form/table/tbody/tr[2]/td/div[2]/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[{i}]/td[11]').text.strip()
            except Exception:
                pass

            summary = fullName + ' is a individual listed by James City County Police Department, Virginia, U.S'

            if fullName:
                data_dict['fullName'] = fullName
                data_dict['gender'] = gender
                data_dict['category'] = 'CRIME'
                data_dict['charges'] = charges
                data_dict['additionalInfo'] = additionalInfo
                data_dict['summary'] = summary
                data_dict['policeStation'] = policeStation
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
