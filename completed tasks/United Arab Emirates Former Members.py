'''
Month_assigned : March
Date Submitted : 29-03-2022
Date_source_name :United Arab Emirates Former Members
Data_source_URL : https://www.almajles.gov.ae/AboutTheFNC/UndertheFNC/Pages/Previous-Members-aspx.aspx
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
from bs4 import BeautifulSoup as soup
import time

last_updated_dev = int(time.time())
update_label_ts = int(time.time())

options = webdriver.ChromeOptions()
prefs = {
    "translate_whitelists": {"ar": "en"},
    "translate": {"enabled": "true"}
}
options.add_experimental_option("prefs", prefs)

PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver\\chromedriver.exe"
driver = webdriver.Chrome(options=options, executable_path=PATH)
driver.maximize_window()


# def to_json(data_list):
#     hash_obj = json.dumps(data_list)
#     with open('json/dictionary.json', 'w') as ts:
#         ts.write(hash_obj)


# def get_soup(url):
#     res = requests.get(url)
#     soup = bs(res.text, 'html.parser')
#     return soup


def get_hash_of_html(html_string):
    hash_object = hashlib.md5(html_string.encode('utf-8'))
    hash_of_html = hash_object.hexdigest()
    return hash_of_html


def extract_entity(data_sec, raw_html, slug_name):
    html_hash = get_hash_of_html(raw_html)

    if data_sec:
        data_dict = {}
        fullName = ''
        city = ''
        designation = ''
        image = ''
        summary = ''
        additionalInfo = ''

        try:
            fullName = data_sec.find_element(By.CSS_SELECTOR, 'h1').text.strip()
            # print(fullName)
        except Exception:
            pass

        try:
            city = data_sec.find_element(By.CSS_SELECTOR,'a.profile-block-loc').text.strip()
            # print(city)
        except Exception:
            pass

        try:
            additionalInfo = data_sec.find_element(By.CSS_SELECTOR,'a.profile-block-trm').text.strip()
            # print(additionalInfo)
        except Exception:
            pass

        try:
            designation = "Federal National Council Member"
        except Exception:
            pass

        try:
            summary = fullName + " is a members of the Federal National Council who served in the " + additionalInfo
        except Exception:
            pass

        try:
            image = data_sec.find_element(By.CSS_SELECTOR,'a.acircss5 > img').get_attribute('src')
            # print(image)
        except Exception:
            pass

        if fullName:
            data_dict['fullName'] = fullName
            data_dict['image'] = image
            data_dict['city'] = city
            data_dict['designation'] = designation
            data_dict['additionalInfo'] = additionalInfo
            data_dict['EmployeeName'] = "Ansuman Sahu"
            data_dict['summary'] = summary
            data_dict['UpdationFlag'] = True
            data_dict['RawHtml'] = html_hash
            data_dict['LastUpdatedDev'] = last_updated_dev
            data_dict['UpdateLabelTs'] = update_label_ts
            print(data_dict)

        return data_dict
    return {}


def get_data(slug_name):
    url = 'https://www.almajles.gov.ae/AboutTheFNC/UndertheFNC/Pages/Previous-Members-aspx.aspx'

    data_list = []

    driver.get(url)
    time.sleep(3)

    driver.find_element(By.CSS_SELECTOR,'#ctl00_msadvfnc_myModal > div > div.smodal-header > span').click()
    time.sleep(1)

    driver.find_element(By.XPATH,
                        f"/html/body/form/div[5]/div/div/div/div/div[2]/div/table/tbody/tr/td/table/tbody/tr/td/div/div/section/div/div[2]/div[2]/select").click()
    time.sleep(1)

    li = driver.find_elements(By.XPATH,
                              f"/html/body/form/div[5]/div/div/div/div/div[2]/div/table/tbody/tr/td/table/tbody/tr/td/div/div/section/div/div[2]/div[2]/select/option")

    for i in range(2, len(li)+1):
        driver.find_element(By.XPATH,
                            f"/html/body/form/div[5]/div/div/div/div/div[2]/div/table/tbody/tr/td/table/tbody/tr/td/div/div/section/div/div[2]/div[2]/select/option[{i}]").click()
        time.sleep(3)

        driver.find_element(By.CSS_SELECTOR, '#ctl00_msadvfnc_myModal > div > div.smodal-header > span').click()
        time.sleep(1)

        try:
            data_section = driver.find_elements(By.CSS_SELECTOR, 'div.profile-block')
            print(len(data_section))
            for data in data_section:
                data_dict = extract_entity(data, str(data), slug_name)
                if data_dict:
                    data_list.append(data_dict)

        except Exception:
            pass

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    print(data_list)
