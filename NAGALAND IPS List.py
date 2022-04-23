'''
Month_assigned : April
Date Submitted : 21-04-2022
Date_source_name : NAGALAND IPS List
Harvesting_URL : https://police.nagaland.gov.in/ips-officers/
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
    url = 'https://police.nagaland.gov.in/ips-officers/'
    driver.get(url)
    time.sleep(1)

    try:
        li = driver.find_elements(By.XPATH, '/html/body/div[2]/article/div/div/div/div/div/div/div[2]/div[2]/div/div/table/tbody/tr')
        # print(len(li))
        for i in range(2, len(li)+1):
            data_dict = {}
            fullName = ''
            dob = ''
            doj = ''
            designation = ''
            educationInfo = ''
            importantDates = ''
            remarks = ''

            try:
                fullName = driver.find_element(By.XPATH, f'/html/body/div[2]/article/div/div/div/div/div/div/div[2]/div[2]/div/div/table/tbody/tr[{i}]/th[2]').text.replace('IPS', '').replace(',', '').strip()
                # print(fullName)
            except Exception:
                pass

            try:
                designation = driver.find_element(By.XPATH, f'/html/body/div[2]/article/div/div/div/div/div/div/div[2]/div[2]/div/div/table/tbody/tr[{i}]/th[3]').text
            except Exception:
                pass

            try:
                dob = driver.find_element(By.XPATH, f'/html/body/div[2]/article/div/div/div/div/div/div/div[2]/div[2]/div/div/table/tbody/tr[{i}]/th[4]').text
            except Exception:
                pass

            try:
                educationInfo = driver.find_element(By.XPATH, f'/html/body/div[2]/article/div/div/div/div/div/div/div[2]/div[2]/div/div/table/tbody/tr[{i}]/th[5]').text
            except Exception:
                pass

            try:
                importantDates = "Date of first entry in to Govt. service: " + driver.find_element(By.XPATH, f'/html/body/div[2]/article/div/div/div/div/div/div/div[2]/div[2]/div/div/table/tbody/tr[{i}]/th[6]').text
            except Exception:
                pass

            try:
                doj = driver.find_element(By.XPATH, f'/html/body/div[2]/article/div/div/div/div/div/div/div[2]/div[2]/div/div/table/tbody/tr[{i}]/th[7]').text
                importantDates += " ,Date of appointment to the present post: " + doj
            except Exception:
                pass

            try:
                remarks = driver.find_element(By.XPATH, f'/html/body/div[2]/article/div/div/div/div/div/div/div[2]/div[2]/div/div/table/tbody/tr[{i}]/th[8]').text
            except Exception:
                pass

            summary = fullName + ' is an IPS Officer of Nagaland appointed on ' + doj

            if fullName:
                data_dict['fullName'] = fullName
                data_dict['category'] = 'Individual'
                data_dict['designation'] = designation
                data_dict['dob'] = dob
                data_dict['importantDates'] = importantDates
                data_dict['educationInfo'] = educationInfo
                data_dict['remarks'] = remarks
                data_dict['state'] = 'Nagaland'
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
    print(data_list)