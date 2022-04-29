'''
Month_assigned : April
Date Submitted :
Date_source_name :
Harvesting_URL : https://www.keysso.net/warrantsA
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
    url = 'https://www.keysso.net/warrantsA'
    driver.get(url)
    time.sleep(1)

    try:
        li = driver.find_elements(By.XPATH, '/html/body/main/div[2]/header/p[4]/a')
        for i in range(1, len(li)+1):
            driver.find_element(By.XPATH, f'/html/body/main/div[2]/header/p[4]/a[{i}]').click()
            time.sleep(1)

            li2 = driver.find_elements(By.XPATH, f'/html/body/main/div[2]/div')
            for j in range(2, len(li2)+1):
                data_dict = {}
                fullName = ''
                fullAddress = ''
                dob = ''
                age = ''
                gender = ''
                height = ''
                weight = ''
                race = ''
                hair = ''
                eyes = ''
                charges = ''
                additionalInfo = ''
                importantDates = ''

                try:
                    temp = driver.find_element(By.XPATH, f'/html/body/main/div[2]/div[{j}]/div[1]').text.strip().replace('Click to see Photo', '').split(',')
                    fullName = " ".join(temp[::-1])
                except Exception:
                    pass

                try:
                    info_list = driver.find_element(By.XPATH, f'/html/body/main/div[2]/div[{j}]/div[2]').text.strip().split("\n")
                    for info in info_list:
                        if 'Dob' in info:
                            dob = info.split(':')[1].replace('Age', '').strip()
                            age = info.split(':')[2].strip()
                        if 'Race' in info:
                            race = info.split(':')[1].replace('Sex', '').strip()
                            gender = info.split(':')[2].strip()
                        if 'Height' in info:
                            height = info.split(':')[1].replace('Weight', '').strip()
                            weight = info.split(':')[2].strip()
                        if 'Hair' in info:
                            hair = info.split(':')[1].replace('Eyes', '').strip()
                            eyes = info.split(':')[2].strip()

                except Exception:
                    pass

                try:
                    fullAddress = driver.find_element(By.XPATH, f'/html/body/main/div[2]/div[{j}]/div[3]').text.strip().replace('\n', ', ')
                except Exception:
                    pass

                try:
                    charges = driver.find_element(By.XPATH, f'/html/body/main/div[2]/div[{j}]/div[4]').text.strip().replace('\n', ', ')
                except Exception:
                    pass

                try:
                    adInfo_list = driver.find_element(By.XPATH, f'/html/body/main/div[2]/div[{j}]/div[5]').text.strip().replace('\n', ' ').split(" ")
                    additionalInfo = "Warrant ID:" + adInfo_list[0] + " " + adInfo_list[2] + adInfo_list[3]
                    importantDates = adInfo_list[1]
                except Exception:
                    pass

                if fullName:
                    data_dict['fullName'] = fullName.replace('\n', '').strip()
                    data_dict['dob'] = dob
                    data_dict['age'] = age
                    data_dict['gender'] = gender
                    data_dict['race'] = race
                    data_dict['height'] = height
                    data_dict['weight'] = weight
                    data_dict['hair'] = hair
                    data_dict['eyes'] = eyes
                    data_dict['fullAddress'] = fullAddress
                    data_dict['importantDates'] = importantDates
                    data_dict['category'] = 'CRIME'
                    data_dict['charges'] = charges
                    data_dict['additionalInfo'] = additionalInfo
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
