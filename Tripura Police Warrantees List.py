'''
Month_assigned : April
Date Submitted : 08-04-2022
Date_source_name : Tripura Police Warrantees List
Harvesting_URL : https://tripurapolice.gov.in/dhalai/wanted
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
    url = 'https://tripurapolice.gov.in/dhalai/wanted'
    driver.get(url)
    time.sleep(1)

    while True:
        try:
            li = driver.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div/section[2]/section/div[2]/div/div[1]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr')
            for i in range(2, len(li)+1):
                data_dict = {}
                fullName = ''
                alias = ''
                familyInfo = ''
                policeStation = ''

                try:
                    temp = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div/section[2]/section/div[2]/div/div[1]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr[{i}]/td[3]').text.strip()
                    temp2 = temp.split('PS')[0]
                    temp3 = ''

                    if 'S/O' in temp2:
                        temp3 = temp2.split('S/O')[0]
                        familyInfo = 'Father\'s Name: ' + temp2.split('S/O')[-1]
                    if 'W/O' in temp2 or 'D/O' in temp2:
                        temp4 = temp2.split('W/O')[0]
                        familyInfo = 'Husband\'s Name: ' + temp2.split('W/O')[-1]
                        temp3 = temp4.split('D/O')[0]
                        if temp4.split('D/O')[-1] != temp3:
                            familyInfo += 'Father\'s Name: ' + temp4.split('D/O')[-1]

                    fullName = temp3.split('@')[0]
                    temp2 = temp3.split('@')[1:]
                    alias = ', '.join(temp2)
                except Exception:
                    pass

                try:
                    policeStation = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div/section[2]/section/div[2]/div/div[1]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr[{i}]/td[2]').text.strip()
                except Exception:
                    pass

                summary = fullName + ' is a wanted individual as recorded by Dhalai District Police, Government of Tripura'

                if fullName:
                    data_dict['fullName'] = fullName
                    data_dict['alias'] = alias
                    data_dict['category'] = 'Individual'
                    data_dict['familyInfo'] = familyInfo
                    data_dict['policeStation'] = policeStation
                    data_dict['state'] = 'Tripura'
                    data_dict['country'] = 'India'
                    data_dict['summary'] = summary
                    # print(data_dict)
                    html_hash = get_hash_of_html(str(data_dict))
                    data_dict['UpdationFlag'] = True
                    data_dict['RawHtml'] = html_hash
                    data_dict['LastUpdatedDev'] = last_updated_dev
                    data_dict['UpdateLabelTs'] = update_label_ts
                    data_list.append(data_dict)

            driver.find_element(By.CSS_SELECTOR, 'li.pager-next > a').click()
            time.sleep(1)

        except Exception:
            break

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