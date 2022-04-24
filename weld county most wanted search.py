'''
Month_assigned : April
Date Submitted : 25-04-2022
Date_source_name : weld county most wanted search
Data_source_URL : https://apps1.weldgov.com/sheriff/mostwanted/
Data_Extractor : Ansuman Sahu
Assinged_cleaner : --
'''

from functools import reduce
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


def get_soup(url):
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')
    return soup


def get_data(slug_name):
    last_updated_dev = int(time.time())
    update_label_ts = int(time.time())

    PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver\\chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(PATH)
    driver.maximize_window()

    data_list = []
    url = 'https://apps1.weldgov.com/sheriff/mostwanted/'
    driver.get(url)
    time.sleep(1)

    li = driver.find_elements(By.XPATH, '/html/body/div/main/div/div[1]/div[2]/div[2]/div[1]/form/select[1]/option')

    for i in range(1, len(li)+1):

        li2 = driver.find_elements(By.XPATH, '/html/body/div/main/div/div[1]/div[2]/div[2]/div[1]/form/select[2]/option')
        for j in range(3, len(li2)+1):
            driver.find_element(By.XPATH, '/html/body/div/main/div/div[1]/div[2]/div[2]/div[1]/form/select[1]').click()
            time.sleep(0.15)
            driver.find_element(By.XPATH, f'/html/body/div/main/div/div[1]/div[2]/div[2]/div[1]/form/select[1]/option[{i}]').click()
            time.sleep(1)

            driver.find_element(By.XPATH, '/html/body/div/main/div/div[1]/div[2]/div[2]/div[1]/form/select[2]').click()
            time.sleep(0.15)
            driver.find_element(By.XPATH, f'/html/body/div/main/div/div[1]/div[2]/div[2]/div[1]/form/select[2]/option[{j}]').click()
            time.sleep(1)

            try:
                driver.find_element(By.XPATH, '/html/body/div/main/div/div[1]/div[2]/div[2]/div[1]/form/input').click()
                time.sleep(1)

                img = driver.find_elements(By.CSS_SELECTOR, 'img.expandedImg')
                image = []
                for images in img:
                    image.append(images.get_attribute('src'))

                page = driver.find_element(By.CSS_SELECTOR, '#mostWantedContent').text
                temp = page.split('VITAL STATISTICS')
                count = 0
                for data_section in temp[1:]:
                    data = [i for i in data_section.split('\n') if i]
                    # print(data[:7])
                    data_dict = {}
                    fullName = data[0].strip()
                    data_dict['fullName'] = fullName
                    data_dict['image'] = image[count]
                    data_dict['dob'] = data[1].replace('DATE OF BIRTH:', '').strip()
                    data_dict['gender'] = data[2].replace('GENDER:', '').strip()
                    data_dict['height'] = data[3].replace('HEIGHT:', '').strip()
                    data_dict['weight'] = data[4].replace('WEIGHT:', '').strip()
                    data_dict['hair'] = data[5].replace('HAIR:', '').strip()
                    data_dict['eyes'] = data[6].replace('EYES:', '').strip()
                    data_dict['summary'] = fullName + " is a Most Wanted individual listed by Weld County, Colorado, U.S"
                    # print(data_dict)
                    html_hash = get_hash_of_html(str(data_dict))
                    data_dict['UpdationFlag'] = True
                    data_dict['RawHtml'] = html_hash
                    data_dict['LastUpdatedDev'] = last_updated_dev
                    data_dict['UpdateLabelTs'] = update_label_ts
                    data_list.append(data_dict)
                    count += 1

            except Exception:
                pass

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    print(data_list)
