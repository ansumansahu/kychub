'''
Month_assigned : April
Date Submitted : 04-04-2022
Date_source_name : Most Wicked Indian Gangsters
Harvesting_URL : https://www.thefamouspeople.com/indian-gangsters.php
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


def to_json(data_list):
    hash_obj = json.dumps(data_list)
    with open('dictionary.json', 'w') as ts:
        ts.write(hash_obj)

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
        image = ''
        dob = ''
        category = ''
        crimeDescription = ''
        placeOfBirthCity = ''
        placeOfBirthCountry = ''
        additionalInfo = ''
        summary = ''

        try:
            fullName = data_sec.find_element(By.CSS_SELECTOR, 'h2 > a').text.strip()
        except Exception:
            pass

        try:
            image = data_sec.find_element(By.CSS_SELECTOR, 'img.img-responsive.combi-profile-img').get_attribute('src')
        except Exception:
            pass

        try:
            summary = data_sec.find_element(By.CSS_SELECTOR, 'div.desc.descEvent').text.strip()
        except Exception:
            pass

        try:
            temp2 = data_sec.find_element(By.CSS_SELECTOR, f'div.col-lg-8.col-md-7.col-sm-7.col-xs-12.rt-text-display').text.strip()
            temp3 = temp2.split("\n")
            for temp in temp3:
                if "Famous As:" in temp:
                    crimeDescription = temp.split(':')[1].replace('"', "").strip()
                if "Birthdate:" in temp:
                    dob = temp.split(':')[1].replace('"', "").strip()
                if "Sun Sign:" in temp:
                    additionalInfo = "Sun Sign: " + temp.split(':')[1].replace('"', "").strip()
                if "Birthplace:" in temp:
                    placeOfBirthCity = temp.split(':')[1].replace('"', "").replace('India', '').replace('British', '').strip()
                    placeOfBirthCountry = 'India'
                if "Died:" in temp:
                    additionalInfo += " Died: " + temp.split(':')[1].replace('"', "").strip()

        except Exception:
            pass

        if not summary:
            summary = fullName + " born on " + dob + " is one of the most wicked Indian Gangsters"

        if fullName:
            data_dict['fullName'] = fullName
            data_dict['image'] = image
            data_dict['dob'] = dob
            data_dict['placeOfBirthCity'] = placeOfBirthCity
            data_dict['placeOfBirthCountry'] = placeOfBirthCountry
            data_dict['category'] = 'Individual'
            data_dict['crimeDescription'] = crimeDescription
            data_dict['additionalInfo'] = additionalInfo
            data_dict['summary'] = summary
            data_dict['UpdationFlag'] = True
            data_dict['RawHtml'] = html_hash
            data_dict['LastUpdatedDev'] = last_updated_dev
            data_dict['UpdateLabelTs'] = update_label_ts
            print(data_dict)

        return data_dict
    return {}


def get_data(slug_name):
    url = 'https://www.thefamouspeople.com/indian-gangsters.php'

    data_list = []
    driver.get(url)
    time.sleep(1)

    try:
        data_section = driver.find_elements(By.CSS_SELECTOR,'article.feature.col-lg-12.col-md-12.col-sm-12.col-xs-12.eventt.internal_space')
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
    to_json(data_list)
    print(data_list)