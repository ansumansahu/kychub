'''
Month_assigned : April
Date Submitted : 07-04-2022
Date_source_name : MALAPPURAM WANTED
Harvesting_URL : https://malappuram.keralapolice.gov.in/public-information/alerts/wanted-persons
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

# def download_pdf(link, k):
#     r = requests.get(link, stream=True)
    # try:
    #     req = requests.get(link)
    # except requests.exceptions.ConnectionError:
    #     r.status_code = "Connection refused"
    # with open(r"D:\test\%s.pdf"%(k) , 'wb') as fd:
    #     for chunk in r.iter_content(1000):
    #         print(chunk)
    #         fd.write(chunk)


def extract_entity(data_sec, raw_html, slug_name):
    html_hash = get_hash_of_html(raw_html)

    if data_sec:
        data_dict = {}
        fullName = ''
        image = ''
        policeStation = ''
        additionalInfo = ''
        summary = ''

        try:
            fullName = data_sec.find_element(By.CSS_SELECTOR, 'h4.media-heading').text.split(',')[0].strip()
        except Exception:
            pass

        try:
            image = data_sec.find_element(By.CSS_SELECTOR, 'div.media > a > img').get_attribute('src')
        except Exception:
            pass

        try:
            summary = data_sec.find_element(By.CSS_SELECTOR, 'div.media-body > p').text.strip()
        except Exception:
            pass

        try:
            pdf = data_sec.find_element(By.CSS_SELECTOR, 'div.media-body > a').get_attribute('href')
            additionalInfo = 'Additional Details: ' + pdf
            # download_pdf(pdf , fullName)
        except Exception:
            pass

        if fullName:
            data_dict['fullName'] = fullName
            data_dict['image'] = image
            data_dict['category'] = 'Individual'
            data_dict['country'] = 'India'
            data_dict['additionalInfo'] = additionalInfo
            data_dict['summary'] = summary
            # print(data_dict)
            html_hash = get_hash_of_html(str(data_dict))
            data_dict['UpdationFlag'] = True
            data_dict['RawHtml'] = html_hash
            data_dict['LastUpdatedDev'] = last_updated_dev
            data_dict['UpdateLabelTs'] = update_label_ts

        return data_dict
    return {}


def get_data(slug_name):
    data_list = []
    url = 'https://malappuram.keralapolice.gov.in/public-information/alerts/wanted-persons'
    driver.get(url)
    time.sleep(1)

    li = driver.find_elements(By.XPATH, f"/html/body/div[2]/div[4]/div[1]/div/div[4]/span/a")

    for i in range(1, len(li)+1):
        driver.find_element(By.XPATH, f"/html/body/div[2]/div[4]/div[1]/div/div[4]/span/a[{i}]").click()
        time.sleep(1)

        try:
            data_section = driver.find_elements(By.CSS_SELECTOR, 'div.media')
            for data in data_section:
                data_dict = extract_entity(data, str(data), slug_name)
                if data_dict:
                    data_list.append(data_dict)

        except Exception:
            pass

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
