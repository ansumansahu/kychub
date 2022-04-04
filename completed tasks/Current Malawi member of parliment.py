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

# options = webdriver.ChromeOptions()
# prefs = {
#     "translate_whitelists": {"ar": "en"},
#     "translate": {"enabled": "true"}
# }
# options.add_experimental_option("prefs", prefs)

PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver\\chromedriver.exe"
# driver = webdriver.Chrome(options=options, executable_path=PATH)
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
        fullName = ''
        title = ''
        designation = ''
        image = ''
        summary = ''
        nationality = ''

        try:
            temp = data_sec.find_element(By.CSS_SELECTOR, 'div.sppb-person-information > span').text.replace(",","").replace("M.P","").replace("MP","").replace(".","").strip()
            fullName = " ".join(temp.split()[1:])
            title = temp.split()[0]
        except Exception:
            pass

        try:
            image = data_sec.find_element(By.CSS_SELECTOR, 'div.sppb-person-image > img').get_attribute('src')
        except Exception:
            pass

        try:
            designation = data_sec.find_element(By.CSS_SELECTOR, 'div.sppb-person-introtext').text.strip()
        except Exception:
            pass

        try:
            summary = title + " " + fullName + " is a current Member of Parliament of Malawi"
        except Exception:
            pass

        if fullName:
            data_dict['title'] = title
            data_dict['fullName'] = fullName
            data_dict['image'] = image
            data_dict['nationality'] = "Malawi"
            data_dict['designation'] = designation
            data_dict['summary'] = summary
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
        url = 'https://www.malawi.gov.mw/index.php/parliament/cabinets'
        driver.get(url)
        time.sleep(1)

        try:
            data_section = driver.find_elements(By.CSS_SELECTOR,'div.sppb-addon-content')
            for data in data_section:
                data_dict = extract_entity(data, str(data), slug_name)
                if data_dict:
                    data_list.append(data_dict)

        except Exception:
            pass

    except Exception:
        pass

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    print(data_list)
