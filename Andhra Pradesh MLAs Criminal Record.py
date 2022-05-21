'''
Month_assigned : April
Date Submitted : 05-04-2022
Date_source_name : Andhra Pradesh MLAs Criminal Record
Harvesting_URL : https://www.oneindia.com/andhra-pradesh-mlas-with-criminal-cases/
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

last_updated_dev = int(time.time())
update_label_ts = int(time.time())

PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver\\chromedriver.exe"
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(PATH)
driver.maximize_window()


def to_json(data_list):
    hash_obj = json.dumps(data_list)
    with open('json/dictionary.json', 'w') as ts:
        ts.write(hash_obj)


def get_hash_of_html(html_string):
    hash_object = hashlib.md5(html_string.encode('utf-8'))
    hash_of_html = hash_object.hexdigest()
    return hash_of_html


# def get_soup(url):
#     res = requests.get(url)
#     soup = bs(res.text, 'html.parser')
#     return soup


def get_data(slug_name):
    data_list = []
    fullName = []
    constituency = []
    politicalPartyName = []
    additionalInfo = []
    educationInfo = []
    assets = []
    try:
        url = 'https://www.oneindia.com/andhra-pradesh-mlas-with-criminal-cases/'
        driver.get(url)
        time.sleep(1)
        li = driver.find_elements(By.XPATH, f'/html/body/section[1]/div/section[1]/div[2]/div[1]/div[2]/div[6]/table/tbody/tr')

        for i in range(2, len(li)+1):
            try:
                temp = driver.find_element(By.XPATH, f"/html/body/section[1]/div/section[1]/div[2]/div[1]/div[2]/div[6]/table/tbody/tr[{i}]/td[3]").text
                fullName.append(temp)
            except Exception:
                pass

            try:
                temp = driver.find_element(By.XPATH, f"/html/body/section[1]/div/section[1]/div[2]/div[1]/div[2]/div[6]/table/tbody/tr[{i}]/td[2]").text
                constituency.append(temp)
            except Exception:
                pass

            try:
                temp = driver.find_element(By.XPATH, f"/html/body/section[1]/div/section[1]/div[2]/div[1]/div[2]/div[6]/table/tbody/tr[{i}]/td[4]").text
                politicalPartyName.append(temp)
            except Exception:
                pass

            try:
                temp = driver.find_element(By.XPATH, f"/html/body/section[1]/div/section[1]/div[2]/div[1]/div[2]/div[6]/table/tbody/tr[{i}]/td[5]").text
                additionalInfo.append("Number of criminal cases: " + temp)
            except Exception:
                pass

    except Exception:
        pass

    try:
        driver.find_element(By.XPATH, '/html/body/section[1]/div/section[1]/div[2]/div[1]/div[1]/div/div[2]/select').click()
        time.sleep(0.5)

        driver.find_element(By.XPATH, '/html/body/section[1]/div/section[1]/div[2]/div[1]/div[1]/div/div[2]/select/option[1]').click()
        time.sleep(1)
        li = driver.find_elements(By.XPATH, f'/html/body/section[1]/div/section[1]/div[2]/div[1]/div[2]/div[6]/table/tbody/tr')

        for i in range(2, len(li)+1):
            try:
                temp = driver.find_element(By.XPATH, f"/html/body/section[1]/div/section[1]/div[2]/div[1]/div[2]/div[6]/table/tbody/tr[{i}]/td[5]").text
                educationInfo.append(temp)
            except Exception:
                pass

    except Exception:
        pass

    try:
        driver.find_element(By.XPATH, '/html/body/section[1]/div/section[1]/div[2]/div[1]/div[1]/div/div[2]/select').click()
        time.sleep(0.5)

        driver.find_element(By.XPATH, '/html/body/section[1]/div/section[1]/div[2]/div[1]/div[1]/div/div[2]/select/option[2]').click()
        time.sleep(1)
        li = driver.find_elements(By.XPATH, f'/html/body/section[1]/div/section[1]/div[2]/div[1]/div[2]/div[6]/table/tbody/tr')

        for i in range(2, len(li) + 1):
            try:
                temp = driver.find_element(By.XPATH, f"/html/body/section[1]/div/section[1]/div[2]/div[1]/div[2]/div[6]/table/tbody/tr[{i}]/td[5]").text
                assets.append(temp)
            except Exception:
                pass

    except Exception:
        pass

    for i in range(len(fullName)):
        data_dict = {}
        data_dict['fullName'] = fullName[i]
        data_dict['constituency'] = constituency[i]
        data_dict['politicalPartyName'] = politicalPartyName[i]
        data_dict['category'] = 'Individual'
        data_dict['country'] = 'India'
        data_dict['educationInfo'] = educationInfo[i]
        data_dict['additionalInfo'] = additionalInfo[i] + ' ,Assets: ' + assets[i]
        data_dict['summary'] = fullName[i] + ' is a Member of the Legislative Assembly of Andhra Pradesh and also a member of ' + politicalPartyName[i] + ' political party'
        # print(data_dict)
        html_hash = get_hash_of_html(str(data_dict))
        data_dict['UpdationFlag'] = True
        data_dict['RawHtml'] = html_hash
        data_dict['LastUpdatedDev'] = last_updated_dev
        data_dict['UpdateLabelTs'] = update_label_ts
        data_list.append(data_dict)

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    print(data_list)
