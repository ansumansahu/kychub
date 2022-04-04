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

PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver\\chromedriver.exe"
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(PATH)
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
        name = ''
        designation = ''
        img = ''
        address = ''
        summary = ''
        email = ''
        phone = ''
        add_info = ''

        try:
            name, designation = data_sec.find_element(By.CSS_SELECTOR, 'h3').text.strip().split('\n')
        except Exception:
            pass

        try:
            address = data_sec.find_element(By.CLASS_NAME, 'carousel-inner').text.strip()
        except Exception:
            pass

        try:
            phone = data_sec.find_element(By.CSS_SELECTOR,'p.phone').text.strip()
        except Exception:
            pass

        try:
            email = data_sec.find_element(By.CSS_SELECTOR,'p.phone.lt').text.strip().replace('\n', ', ')
        except Exception:
            pass

        try:
            li = data_sec.find_elements(By.CSS_SELECTOR,'p.social.grey a')
            temp = ''
            for ele in li:
                temp += ele.get_attribute('href') + ", "
            if temp:
                add_info = "Social URLs: " + temp.strip()[:-1]
        except Exception:
            pass

        try:
            summary = name.strip() + " is a member of Bharati Janata Party(BJP), India."
        except Exception:
            pass

        try:
            img = data_sec.find_element(By.CLASS_NAME,'fullwidth').get_attribute('src')
        except Exception:
            pass

        if name:
            data_dict['fullName'] = name
            data_dict['image'] = img
            data_dict['designation'] = designation
            data_dict['fullAddress'] = address
            data_dict['telephoneNos'] = phone
            data_dict['emails'] = email
            data_dict['additionalInfo'] = add_info
            data_dict['summary'] = summary
            data_dict['EmployeeName'] = "Ansuman Sahu"
            data_dict['UpdationFlag'] = False
            data_dict['RawHtml'] = html_hash
            data_dict['LastUpdatedDev'] = last_updated_dev
            data_dict['UpdateLabelTs'] = update_label_ts

        return data_dict
    return {}


def get_data(slug_name):
    url = 'https://www.bjp.org/state-prabhari'

    data_list = []

    driver.get(url)
    time.sleep(1)

    driver.find_element(By.XPATH,f"/html/body/div[2]/div[1]/div/div/div/section/div/div/div/div[1]/div[1]/div/form/div[1]/select").click()
    time.sleep(1)

    li = driver.find_elements(By.XPATH,f"/html/body/div[2]/div[1]/div/div/div/section/div/div/div/div[1]/div[1]/div/form/div[1]/select/option")
    for i in range(2,len(li)+1):
        driver.find_element(By.XPATH,f"/html/body/div[2]/div[1]/div/div/div/section/div/div/div/div[1]/div[1]/div/form/div[1]/select/option[{i}]").click()
        time.sleep(1)

        try:
            data_section = driver.find_elements(By.CSS_SELECTOR,'div.col-lg-12.bg-white.col-sm-12.col-md-12.col-12')
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