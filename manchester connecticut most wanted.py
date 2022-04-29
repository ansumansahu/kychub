'''
Month_assigned : April
Date Submitted : 27-04-2022
Date_source_name : manchester connecticut most wanted
Data_source_URL : https://www.bailcobailbonds.com/wanted-fugitives/
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

    data_list = []
    url = 'https://www.bailcobailbonds.com/wanted-fugitives/'
    driver.get(url)
    time.sleep(1)

    try:
        data_sec = driver.find_elements(By.CSS_SELECTOR, 'div.ab-block-layout-column-inner')
        for data in data_sec:
            data_dict = {}
            fullName = ''
            alias = ''
            charges = ''
            height = ''
            weight = ''
            dob = ''
            gender = ''
            race = ''
            hair = ''
            eyes = ''
            distinguishMarks = ''
            policeStation = ''
            additionalInfo = ''

            try:
                link = data.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                soup = get_soup(link)

                try:
                    fullName = soup.find('h1', {'class': 'entry-title'}).text.strip()
                except Exception:
                    pass

                try:
                    text = soup.find('div', {'class': 'ab-container-content'}).text.split('Case')
                    desc = text[0].replace('Description', '').strip()
                    temp = desc.split(':')
                    height = temp[1].replace('Weight', '').strip()
                    weight = temp[2].replace('DOB', '').strip()
                    dob = temp[3].replace('Sex', '').strip()
                    gender = temp[4].replace('Race', '').strip()
                    race = temp[5].replace('Hair Color', '').strip()
                    hair = temp[6].replace('Eye Color', '').strip()
                    eyes = temp[7].replace('Marks/Scars', '').strip()
                    distinguishMarks = temp[8].replace('Tattoos', '').strip()
                    distinguishMarks += ' ,Tattoos: ' + temp[9].replace('Aliases', '').strip()
                    alias = temp[10].strip()

                    text2 = (text[1]).split('Information')
                    case = text2[0].strip()
                    temp2 = case.split(':')
                    policeStation = temp2[1].replace('Court', '').strip()
                    additionalInfo = "Court: " + temp2[2].strip()

                    text3 = (text2[1]).split('Do not try to apprehend this individual')
                    info = text3[0].strip()
                    temp3 = info.split(':')
                    charges = temp3[1].replace('Last Seen', '').strip()
                    additionalInfo += " ,Last Seen: " + temp3[2].replace('Misc Info', '').strip()
                    additionalInfo += " ,Misc Info: " + temp3[3].strip()

                except Exception:
                    pass

                if fullName:
                    data_dict['fullName'] = fullName
                    data_dict['gender'] = gender
                    data_dict['alias'] = alias
                    data_dict['dob'] = dob
                    data_dict['height'] = height
                    data_dict['weight'] = weight
                    data_dict['race'] = race
                    data_dict['eyes'] = eyes
                    data_dict['hair'] = hair
                    data_dict['distinguishMarks'] = distinguishMarks
                    data_dict['charges'] = charges
                    data_dict['policeStation'] = policeStation
                    data_dict['category'] = 'CRIME'
                    data_dict['additionalInfo'] = additionalInfo
                    data_dict['summary'] = fullName + " is a Most Wanted Fugitive listed by BailCo Bail Bonds Manchester LLC, Connecticut, U.S"
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

    except Exception:
        pass

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    # print(data_list)
