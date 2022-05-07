'''
Month_assigned : May
Date Submitted : 05-05-2022
Date_source_name : Meghalaya Officers
Harvesting_URL : https://megpolice.gov.in/meghalaya-police-servicemps-officers
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
    url = 'https://megpolice.gov.in/meghalaya-police-servicemps-officers'
    driver.get(url)
    time.sleep(1)

    try:
        li = driver.find_elements(By.XPATH, '/html/body/div[2]/div[4]/div[2]/div/div[1]/div/div/div/div/div/div/div/div/table/thead/tr')
        for i in range(2, len(li)+1):
            data_dict = {}
            fullName = ''
            title = ''
            image = ''
            designation = ''
            careerInfoStartYear = ''

            try:
                temp = driver.find_element(By.XPATH, f'/html/body/div[2]/div[4]/div[2]/div/div[1]/div/div/div/div/div/div/div/div/table/thead/tr[{i}]/td[1]').text.replace('MPS', '').replace(',', '').strip()
                fullName = " ".join(temp.split(" ")[1:]).strip()
                title = temp.split(" ")[0].strip()
            except Exception:
                pass

            try:
                careerInfoStartYear = driver.find_element(By.XPATH, f'/html/body/div[2]/div[4]/div[2]/div/div[1]/div/div/div/div/div/div/div/div/table/thead/tr[{i}]/td[2]').text.strip()
            except Exception:
                pass

            try:
                designation = driver.find_element(By.XPATH, f'/html/body/div[2]/div[4]/div[2]/div/div[1]/div/div/div/div/div/div/div/div/table/thead/tr[{i}]/td[3]').text.strip()
            except Exception:
                pass

            try:
                image = driver.find_element(By.XPATH, f'/html/body/div[2]/div[4]/div[2]/div/div[1]/div/div/div/div/div/div/div/div/table/thead/tr[{i}]/td[4]/img').get_attribute('src')
            except Exception:
                pass

            summary = fullName + ' is a Meghalaya Police Service(MPS) Officer'

            if fullName:
                data_dict['fullName'] = fullName
                data_dict['title'] = title
                data_dict['image'] = image
                data_dict['designation'] = designation
                data_dict['careerInfoStartYear'] = careerInfoStartYear
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
