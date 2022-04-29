'''
Month_assigned : April
Date Submitted : 28-04-2022
Date_source_name : YSR Congress MLPs
Harvesting_URL : https://www.ysrcongress.com/english/mp
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
    url = 'https://www.ysrcongress.com/english/mp'
    driver.get(url)
    time.sleep(1)

    try:
        li = driver.find_elements(By.XPATH, '/html/body/div[2]/section[3]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr')
        for i in range(1, len(li)+1):
            data_dict = {}
            fullName = ''
            title = ''
            designation = ''
            additionalInfo = ''

            try:
                temp = driver.find_element(By.XPATH, f'/html/body/div[2]/section[3]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[{i}]/td[2]').text.strip()
                title = temp.split(" ")[0]
                fullName = " ".join(temp.split(" ")[1:])
            except Exception:
                pass

            try:
                designation = driver.find_element(By.XPATH, f'/html/body/div[2]/section[3]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[{i}]/td[3]').text.strip()
            except Exception:
                pass

            try:
                additionalInfo = "Location: " + driver.find_element(By.XPATH, f'/html/body/div[2]/section[3]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[{i}]/td[4]').text.strip()
            except Exception:
                pass

            summary = fullName + ' is a Member of Parliament in the Lok Sabha belonging to YSR political party'

            if fullName:
                data_dict['fullName'] = fullName
                data_dict['title'] = title
                data_dict['category'] = 'PEP'
                data_dict['designation'] = designation
                data_dict['politicalPartyName'] = 'YSR'
                data_dict['additionalInfo'] = additionalInfo
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
