'''
Month_assigned : April
Date Submitted : 08-04-2022
Date_source_name : Tripura Police Most Wanted
Harvesting_URL : https://tripurapolice.gov.in/WantedCriminal
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
    data_list = []
    url = 'https://tripurapolice.gov.in/WantedCriminal'
    driver.get(url)
    time.sleep(1)

    li = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/section[2]/section/div[2]/div/div[2]/div/div/div/table/tbody/tr')
    for i in range(1, len(li)+1):
        data_dict = {}
        fullName = ''
        alias = ''
        image = ''
        age = ''
        gender = ''
        eyes = ''
        hair = ''
        height = ''
        weight = ''
        buildCharacteristic = ''
        maritalStatus = ''
        distinguishMarks = ''
        familyInfo = ''
        fullAddress = ''
        additionalInfo = ''
        reward = ''

        try:
            fullName = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/section[2]/section/div[2]/div/div[2]/div/div/div/table/tbody/tr[{i}]/td[2]').text.strip()
        except Exception:
            pass

        try:
            alias = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/section[2]/section/div[2]/div/div[2]/div/div/div/table/tbody/tr[{i}]/td[3]').text.replace('@', ',').strip()
        except Exception:
            pass

        try:
            image = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/section[2]/section/div[2]/div/div[2]/div/div/div/table/tbody/tr[{i}]/td[1]/a').get_attribute('href')
        except Exception:
            pass

        try:
            additionalInfo = 'Group: ' + driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/section[2]/section/div[2]/div/div[2]/div/div/div/table/tbody/tr[{i}]/td[4]').text.strip()
        except Exception:
            pass

        try:
            reward = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/section[2]/section/div[2]/div/div[2]/div/div/div/table/tbody/tr[{i}]/td[5]').text.strip()
        except Exception:
            pass

        try:
            driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/section[2]/section/div[2]/div/div[2]/div/div/div/table/tbody/tr[{i}]/td[2]/a').click()
            time.sleep(1)

            li2 = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/section[2]/section/div[2]/div/div/div/div/div')
            for j in range(1, len(li2)+1):
                temp = driver.find_element(By.XPATH , f'/html/body/div[1]/div/div/section[2]/section/div[2]/div/div/div/div/div[{j}]').text.strip()
                if 'Father\'s Name:' in temp:
                    familyInfo = temp.replace('\n', '')
                if 'Address:' in temp:
                    fullAddress = temp.split(':')[1].strip()
                if 'Age:' in temp:
                    age = temp.split(':')[1].strip()
                if 'Sex:' in temp:
                    gender = temp.split(':')[1].strip()
                if 'Hair:' in temp:
                    hair = temp.split(':')[1].strip()
                if 'Eyes:' in temp:
                    eyes = temp.split(':')[1].strip()
                if 'Height:' in temp:
                    height = temp.split(':')[1].strip()
                if 'Weight:' in temp:
                    weight = temp.split(':')[-1].strip()
                if 'Built & Complextion:' in temp:
                    buildCharacteristic = temp.split(':')[1].strip()
                if 'Marital Status:' in temp:
                    maritalStatus = temp.split(':')[1].strip()
                if 'Identification Mark:' in temp:
                    distinguishMarks = temp.split(':')[1].strip()
                if 'Government Notification No.:' in temp:
                    additionalInfo += temp.replace('\n', '')

            driver.back()
            time.sleep(1)

        except Exception:
            pass

        summary = fullName + ' is a wanted individual in the records of Tripura Police with a reward of ' + reward + ' for reporting.'

        if fullName:
            data_dict['fullName'] = fullName
            data_dict['category'] = 'Individual'
            data_dict['alias'] = alias
            data_dict['image'] = image
            data_dict['age'] = age
            data_dict['gender'] = gender
            data_dict['eyes'] = eyes
            data_dict['hair'] = hair
            data_dict['height'] = height
            data_dict['weight'] = weight
            data_dict['buildCharacteristic'] = buildCharacteristic
            data_dict['distinguishMarks'] = distinguishMarks
            data_dict['maritalStatus'] = maritalStatus
            data_dict['familyInfo'] = familyInfo
            data_dict['fullAddress'] = fullAddress
            data_dict['state'] = 'Tripura'
            data_dict['country'] = 'India'
            data_dict['additionalInfo'] = additionalInfo
            data_dict['reward'] = reward
            data_dict['summary'] = summary
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

    last_updated_dev = int(time.time())
    update_label_ts = int(time.time())

    PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver\\chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(PATH)
    driver.maximize_window()

    data_list = get_data('add-slug-here')
    # to_json(data_list)
    print(data_list)