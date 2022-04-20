'''
Month_assigned : April
Date Submitted : 19-04-2022
Date_source_name : AICC Secretaries
Harvesting_URL : https://www.inc.in/aicc-office-bearers/secretaries
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
        image = ''
        fullAddress = ''
        designation = ''
        telephoneNos = ''
        mobileNos = ''
        emails = ''
        summary = ''

        try:
            fullName = data_sec.find_element(By.CSS_SELECTOR, 'h6.MuiTypography-root.blue.aicc_title').text.strip()
        except Exception:
            pass

        try:
            designation = data_sec.find_element(By.CSS_SELECTOR, 'h5').text.strip()
        except Exception:
            pass

        try:
            image = data_sec.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
        except Exception:
            pass

        try:
            fullAddress = data_sec.find_element(By.CSS_SELECTOR, 'h6.MuiTypography-root.aicc_address').text.strip()
        except Exception:
            pass

        try:
            temp = data_sec.find_element(By.CSS_SELECTOR, 'div.MuiGrid-root.aicc_bearers_details').text
            temp2 = temp.split('\n')
            for line in temp2:
                if '(O):' in line:
                    telephoneNos = line.replace('(O):', '').strip()
                if '(M):' in line:
                    mobileNos = line.replace('(M):', '').strip()
                if '(E)' in line:
                    emails += line.replace('(E)', '').strip() + ", "
        except Exception:
            pass

        summary = fullName + " is one of the Secretaries and also a Member of All India Congress Committee"

        if fullName:
            data_dict['fullName'] = fullName
            data_dict['image'] = image
            data_dict['category'] = 'Individual'
            data_dict['fullAddress'] = fullAddress
            data_dict['telephoneNos'] = telephoneNos
            data_dict['mobileNos'] = mobileNos
            data_dict['emails'] = emails
            data_dict['politicalPartyName'] = 'All India Congress Committee'
            data_dict['designation'] = designation
            data_dict['country'] = 'India'
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
    url = 'https://www.inc.in/aicc-office-bearers/secretaries'
    driver.get(url)
    time.sleep(1)

    try:
        data_section = driver.find_elements(By.CSS_SELECTOR, 'div.MuiGrid-root.aicc_bearers_outer_block')
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
