'''
Month_assigned : April
Date Submitted : 27-04-2022
Date_source_name : crime watch delaware warrants
Data_source_URL : https://delaware.crimewatchpa.com/warrants
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

    url = 'https://delaware.crimewatchpa.com/warrants'
    data_list = []
    driver.get(url)
    time.sleep(1)

    while True:
        try:
            driver.find_element(By.CSS_SELECTOR, 'li.pager__item').click()
            time.sleep(1)
        except Exception:
            break

    try:
        data_secs = driver.find_elements(By.CSS_SELECTOR,'table.views-table.sticky-enabled.cols-6.tableheader-processed.sticky-table tbody tr')
        for data_sec in data_secs:
            if data_sec:
                data_dict = {}
                fullName = ''
                additionalInfo = ''
                importantDates = ''
                charges = ''

                try:
                    tds = data_sec.find_elements(By.CSS_SELECTOR, 'td')
                    temp = tds[0].text.strip()
                    charges = temp.split("-", 1)[-1].lower()
                    fullName = temp.split("-", 1)[0]
                    temp = tds[2].text.strip()
                    if temp:
                        if additionalInfo:
                            additionalInfo += "; "
                        additionalInfo += "Type: " + temp
                    temp = tds[3].text.strip()
                    if temp:
                        if additionalInfo:
                            additionalInfo += "; "
                        additionalInfo += "Docket No.: " + temp
                    temp = tds[4].text.strip()
                    if temp:
                        if importantDates:
                            importantDates += "; "
                        importantDates += "Date Issued: " + temp
                    temp = tds[5].text.strip()
                    if temp:
                        if additionalInfo:
                            additionalInfo += "; "
                        additionalInfo += "Holding Department: " + temp
                except Exception:
                    pass

                if fullName:
                    data_dict['fullName'] = fullName.strip()
                    data_dict['charges'] = charges.strip()
                    data_dict['category'] = 'CRIME'
                    data_dict['importantDates'] = importantDates.strip()
                    data_dict['additionalInfo'] = additionalInfo.strip()
                    data_dict['summary'] = fullName + " is a criminal charged for " + charges + "."
                    # print(data_dict)
                    data_dict['UpdationFlag'] = True
                    html_hash = get_hash_of_html(str(data_dict))
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
    data_list = get_data('slug')
    # to_json(data_list)
    # print(data_list)

