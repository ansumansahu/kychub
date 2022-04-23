'''
Month_assigned : April
Date Submitted : 20-04-2022
Date_source_name : NAGALAND COUNCIL OF MINISTERS
Harvesting_URL : https://www.sarkaritel.com/states/council_of_ministers.php?state=NL
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


def extract_entity(data_sec, raw_html, slug_name):
    last_updated_dev = int(time.time())
    update_label_ts = int(time.time())
    html_hash = get_hash_of_html(raw_html)

    if data_sec:
        data_dict = {}
        fullName = ''
        designation = ''
        image = ''
        fullAddress = ''
        telephoneNos = ''
        politicalPartyName = ''
        constituency = ''
        additionalInfo = ''
        summary = ''

        try:
            image = data_sec.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
        except Exception:
            pass

        text = data_sec.text
        for line in text.split('\n'):
            # print(line)
            if 'Name:' in line:
                fullName = line.replace('Name:', '').strip()
                # print(fullName)
            if 'Minister for' in line:
                designation = line.strip()
            if 'Office Address' in line:
                additionalInfo = line.replace(',', '').replace('-', '').strip()
            if 'Office Phone' in line:
                additionalInfo += ' ,' + line.strip()
            if 'Residence Address' in line:
                fullAddress = line.replace('Residence Address :', '').replace(',', '').replace('-', '').strip()
            if 'Residence Phone :' in line:
                telephoneNos = line.replace('Residence Phone :', '').strip()
            if 'Party :' in line:
                politicalPartyName = line.replace('Party :', '').strip()
            if 'Constituency :' in line:
                constituency = line.replace('Constituency :', '').strip()

        summary = fullName + " is a Council of Minister Member of Nagaland and also a member of " + politicalPartyName + " political party"

        if fullName:
            data_dict['fullName'] = fullName
            data_dict['image'] = image
            data_dict['category'] = 'Individual'
            data_dict['fullAddress'] = fullAddress
            data_dict['designation'] = designation
            data_dict['telephoneNos'] = telephoneNos
            data_dict['politicalPartyName'] = politicalPartyName
            data_dict['constituency'] = constituency
            data_dict['state'] = 'Nagaland'
            data_dict['country'] = 'India'
            data_dict['additionalInfo'] = additionalInfo
            data_dict['summary'] = summary
            # print(data_dict)
            html_hash = get_hash_of_html(str(data_dict))
            data_dict['UpdationFlag'] = True
            data_dict['RawHtml'] = html_hash
            data_dict['LastUpdatedDev'] = last_updated_dev
            data_dict['UpdateLabelTs'] = update_label_ts

        return data_dict
    return {}


def get_data(slug_name):
    PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver\\chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(PATH)
    driver.maximize_window()

    data_list = []
    url = 'https://www.sarkaritel.com/states/council_of_ministers.php?state=NL'
    driver.get(url)
    time.sleep(1)

    try:
        data_section = driver.find_elements(By.XPATH, '/html/body/div/div/div[2]/div/div[3]/div/div[2]/div[1]/div/div/div/div/table/tbody/tr/td/table/tbody')
        for data in data_section:
            data_dict = extract_entity(data, str(data), slug_name)
            if data_dict:
                data_list.append(data_dict)

    except Exception:
        pass

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    print(data_list)
