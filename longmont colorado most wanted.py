'''
Month_assigned : April
Date Submitted : 22-04-2022
Date_source_name : longmont colorado most wanted
Harvesting_URL : https://www.longmontcolorado.gov/departments/departments-n-z/public-safety-department/public-safety-services/crime-information/most-wanted
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
    url = 'https://www.longmontcolorado.gov/departments/departments-n-z/public-safety-department/public-safety-services/crime-information/most-wanted'
    driver.get(url)
    time.sleep(1)
    while True:
        try:
            data_section = driver.find_elements(By.XPATH, '/html/body/div[9]/div[2]/div[2]/div[3]/div[2]/table/tbody/tr')
            for data in data_section:
                if data:
                    data_dict = {}
                    fullName = ''
                    image = ''
                    dob = ''
                    gender = ''
                    height = ''
                    weight = ''
                    hair = ''
                    eyes = ''
                    wantedFor = ''

                    text = data.text
                    fullName = text.split('DOB')[0].strip()

                    try:
                        image = data.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                    except Exception:
                        pass

                    try:
                        temp0 = data.text.split('WANTED FOR')[0]
                        for line in temp0.split('\n'):
                            if 'DOB' in line:
                                dob = line.replace('DOB', '').strip()
                            if 'lbs' in line:
                                temp2 = line.split(',')
                                height = temp2[-2].strip()
                                weight = temp2[-1].strip()
                                try:
                                    gender = temp2[-3].strip()
                                except Exception:
                                    pass
                            if 'eyes' in line:
                                temp3 = line.split(',')
                                hair = temp3[0].strip()
                                eyes = temp3[1].strip()
                    except Exception:
                        pass

                    try:
                        wantedFor = data.text.split('WANTED FOR')[1].replace(':', '').strip()
                    except Exception:
                        pass

                    if fullName:
                        data_dict['fullName'] = fullName
                        data_dict['image'] = image
                        data_dict['gender'] = gender
                        data_dict['category'] = 'Individual'
                        data_dict['dob'] = dob
                        data_dict['height'] = height
                        data_dict['weight'] = weight
                        data_dict['hair'] = hair
                        data_dict['eyes'] = eyes
                        data_dict['wantedFor'] = wantedFor
                        data_dict['summary'] = fullName + " is a Most Wanted individual as listed by city of Longmont, Colorado, United States"
                        html_hash = get_hash_of_html(str(data_dict))
                        data_dict['UpdationFlag'] = True
                        data_dict['RawHtml'] = html_hash
                        data_dict['LastUpdatedDev'] = last_updated_dev
                        data_dict['UpdateLabelTs'] = update_label_ts

                    if data_dict:
                        data_list.append(data_dict)

            driver.find_element(By.XPATH, '/html/body/div[9]/div[2]/div[2]/div[3]/div[2]/p[2]/a').click()
            time.sleep(1)

        except Exception:
            break

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    print(data_list)
