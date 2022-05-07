'''
Month_assigned : May
Date Submitted : 06-05-2022
Date_source_name : mansfield most wanted
Harvesting_URL : https://p2c.mansfieldtexas.gov/mostwanted.aspx
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
    name_list = []
    url = 'https://p2c.mansfieldtexas.gov/mostwanted.aspx'
    driver.get(url)
    time.sleep(1)

    while True:
        try:
            data_dict = {}
            fullName = ''
            image = ''
            race = ''
            gender = ''
            age = ''
            height = ''
            weight = ''
            distinguishMarks = ''
            wantedFor = ''
            importantDates = ''
            summary = ''

            try:
                fullName = driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]/table/tbody/tr/td[1]/h2').text.strip()
            except Exception:
                pass

            try:
                image = driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]/table/tbody/tr/td[1]/img').get_attribute('src')
            except Exception:
                pass

            try:
                temp = driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]/table/tbody/tr/td[1]/table/tbody').text
                for line in temp.split("\n"):
                    if "Race" in line:
                        race = line.split(":")[1].strip()
                    if "Sex" in line:
                        gender = line.split(":")[1].strip()
                    if "Age" in line:
                        age = line.split(":")[1].strip()
                    if "lbs" in line:
                        height = " ".join(line.split(" ")[0:2])
                        weight = " ".join(line.split(" ")[2:])
            except Exception:
                pass

            try:
                wantedFor = driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]/table/tbody/tr/td[2]/div[1]/span/font[2]').text.strip()
            except Exception:
                pass

            try:
                importantDates = "Warrant Issued Date : " + driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]/table/tbody/tr/td[2]/div[1]/span/font[4]').text.strip()
            except Exception:
                pass

            summary = fullName + "is a Most Wanted Individual listed by Mansfield Police Department"

            if fullName not in name_list:
                data_dict['fullName'] = fullName
                data_dict['image'] = image
                data_dict['category'] = 'CRIME'
                data_dict['age'] = age
                data_dict['gender'] = gender
                data_dict['race'] = race
                data_dict['height'] = height
                data_dict['weight'] = weight
                data_dict['wantedFor'] = wantedFor
                data_dict['importantDates'] = importantDates
                data_dict['summary'] = summary
                # print(data_dict)
                html_hash = get_hash_of_html(str(data_dict))
                data_dict['UpdationFlag'] = True
                data_dict['RawHtml'] = html_hash
                data_dict['LastUpdatedDev'] = last_updated_dev
                data_dict['UpdateLabelTs'] = update_label_ts
                name_list.append(fullName)
                data_list.append(data_dict)
            else:
                break

            driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]/div/input[2]').click()
            time.sleep(1)

        except Exception:
            break

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    # print(data_list)
