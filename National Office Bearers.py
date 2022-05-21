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

    url = 'https://www.bjp.org/national-office-bearer'
    data_list = []
    driver.get(url)
    time.sleep(1)

    try:
        data_section = driver.find_elements(By.CSS_SELECTOR, 'div.col-lg-3.col-sm-12.col-md-6.col-12')
        for data in data_section:
            if data:
                data_dict = {}
                fullName = ''
                title = ''
                image = ''
                fullAddress = ''
                summary = ''
                emails = ''
                website = ''
                designation = ''
                telephoneNos = ''
                additionalInfo = ''

                try:
                    temp, designation = data.find_element(By.CSS_SELECTOR, 'h3').text.strip().split('\n')
                    title = temp.split(' ')[0]
                    fullName = " ".join(temp.split(' ')[1:])
                except Exception:
                    pass

                try:
                    fullAddress = data.find_element(By.CLASS_NAME, 'carousel-inner').text
                except Exception:
                    pass

                try:
                    telephoneNos = data.find_element(By.CSS_SELECTOR, 'p.phone.l1').text.strip()
                except Exception:
                    pass

                try:
                    emails = data.find_element(By.CSS_SELECTOR, 'p.phone.lt').text.strip().replace('\n', ', ')
                except Exception:
                    pass

                try:
                    website = data.find_element(By.CSS_SELECTOR, 'p.phone.lb').text.strip()
                except Exception:
                    pass

                try:
                    li = data.find_elements(By.CSS_SELECTOR, 'p.social.grey a')
                    temp = ''
                    for ele in li:
                        temp += ele.get_attribute('href') + ", "
                    if temp:
                        additionalInfo = "Social URLs: " + temp.strip()[:-1]
                except Exception:
                    pass

                try:
                    summary = fullName.strip() + " is a member of Bharati Janata Party(BJP), India."
                except Exception:
                    pass

                try:
                    image = data.find_element(By.CLASS_NAME, 'fullwidth').get_attribute('src')
                except Exception:
                    pass

                if fullName:
                    data_dict['fullName'] = fullName
                    data_dict['title'] = title
                    data_dict['image'] = image
                    data_dict['category'] = 'Individual'
                    data_dict['designation'] = designation
                    data_dict['fullAddress'] = fullAddress
                    data_dict['telephoneNos'] = telephoneNos
                    data_dict['emails'] = emails
                    data_dict['website'] = website
                    data_dict['additionalInfo'] = additionalInfo.strip()
                    data_dict['summary'] = summary.strip()
                    html_hash = get_hash_of_html(str(data_dict))
                    data_dict['UpdationFlag'] = True
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
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    print(data_list)
