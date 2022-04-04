'''
Month_assigned : March
Date Submitted : 30-03-2022
Date_source_name : Parliament of Zimbabwe Senetors
Data_source_URL : https://parlzim.gov.zw/senators/
Data_Extractor : Ansuman Sahu
Assinged_cleaner : --
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

last_updated_dev = int(time.time())
update_label_ts = int(time.time())

PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver\\chromedriver.exe"
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(PATH)
driver.maximize_window()


# def to_json(data_list):
#     hash_obj = json.dumps(data_list)
#     with open('json/dictionary.json', 'w') as ts:
#         ts.write(hash_obj)


def get_hash_of_html(html_string):
    hash_object = hashlib.md5(html_string.encode('utf-8'))
    hash_of_html = hash_object.hexdigest()
    return hash_of_html


# def get_soup(url):
#     res = requests.get(url)
#     soup = bs(res.text, 'html.parser')
#     return soup


def extract_entity(data_sec, slug_name):

    if data_sec:
        data_dict = {}
        fullName = ''
        title = ''
        image = ''
        designation = ''
        constituency = ''
        country = ''
        summary = ''

        try:
            fullName = data_sec.find_element(By.CSS_SELECTOR, 'div.team-author > div').text.replace("HON", "").strip()
        except Exception:
            pass

        # try:
        #     image = data_sec.find_element(By.CSS_SELECTOR, 'div.team-media > a > img').get_attribute('src')
        # except Exception:
        #     pass

        try:
            temp = data_sec.find_element(By.CSS_SELECTOR, 'div.team-author > p').text.strip()
            designation = temp.split(':')[1].replace("Constituency","").strip()
            constituency = temp.split(':')[-1].strip()
        except Exception:
            pass

        try:
            summary = fullName + " is a Member of Parliament of Zimbabwe"
        except Exception:
            pass

        if fullName:
            data_dict['title'] = 'HON'
            data_dict['fullName'] = fullName
            # data_dict['image'] = image
            data_dict['designation'] = designation
            data_dict['constituency'] = constituency
            data_dict['country'] = 'Zimbabwe'
            data_dict['summary'] = summary
            html_hash = get_hash_of_html(str(data_dict))
            data_dict['EmployeeName'] = "Ansuman Sahu"
            data_dict['UpdationFlag'] = True
            data_dict['RawHtml'] = html_hash
            data_dict['LastUpdatedDev'] = last_updated_dev
            data_dict['UpdateLabelTs'] = update_label_ts
            print(data_dict)

        return data_dict
    return {}


def get_data(slug_name):
    data_list = []
    try:
        url = 'https://parlzim.gov.zw/senators/'
        driver.get(url)
        time.sleep(5)

        while True:
            try:
                data_section = driver.find_elements(By.XPATH,f'/html/body/div[2]/div[6]/div[2]/div/div/div/div[3]/div/div/div/div/div[2]/div/div')
                for data in data_section:
                    data_dict = extract_entity(data, slug_name)
                    if data_dict:
                        data_list.append(data_dict)

            except Exception:
                pass

            driver.find_element(By.CSS_SELECTOR, f'a.page-numbers.nav-next > i').click()
            time.sleep(5)

    except Exception:
        pass

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    print(data_list)
