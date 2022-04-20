'''
Month_assigned : April
Date Submitted : 18-04-2022
Date_source_name : santa barbara most wanted
Harvesting_URL : https://www.sbsheriff.org/category/wanted-subject/
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
    url = 'https://www.sbsheriff.org/category/wanted-subject/'
    driver.get(url)
    time.sleep(1)

    while True:
        try:
            li = driver.find_elements(By.XPATH, '/html/body/div[6]/div[1]/div/div[2]/p/a')
            for i in range(1, len(li)+1):
                try:
                    driver.find_element(By.XPATH, f'/html/body/div[6]/div[1]/div[{i}]/div[2]/p/a').click()
                    time.sleep(1)

                    data_dict = {}
                    importantDates = ''
                    image = ''
                    additionalInfo = ''

                    try:
                        importantDates = driver.find_element(By.CSS_SELECTOR, 'div.article-header.entry-header > p').text
                    except Exception:
                        pass

                    try:
                        image = driver.find_element(By.CSS_SELECTOR, 'div.entry-content.cf > img').get_attribute('src')
                    except Exception:
                        pass

                    try:
                        additionalInfo = driver.find_element(By.CSS_SELECTOR, 'div.entry-content.cf > p').text
                    except Exception:
                        pass

                    summary = 'A wanted individual as recorded by Santa Barbara County, California, U.S'

                    if image:
                        data_dict['image'] = image
                        data_dict['category'] = 'Individual'
                        data_dict['additionalInfo'] = additionalInfo
                        data_dict['importantDates'] = importantDates
                        data_dict['city'] = 'Santa Barbara'
                        data_dict['state'] = 'California'
                        data_dict['country'] = 'United States'
                        data_dict['summary'] = summary
                        # print(data_dict)
                        html_hash = get_hash_of_html(str(data_dict))
                        data_dict['UpdationFlag'] = True
                        data_dict['RawHtml'] = html_hash
                        data_dict['LastUpdatedDev'] = last_updated_dev
                        data_dict['UpdateLabelTs'] = update_label_ts
                        data_list.append(data_dict)

                    driver.back()
                    time.sleep(1)

                except Exception:
                    pass

            driver.find_element(By.CSS_SELECTOR, 'a.next').click()

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