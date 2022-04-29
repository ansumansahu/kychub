'''
Month_assigned : April
Date Submitted : 28-04-2022
Date_source_name : US immigration and customs wanted list
Data_source_URL : https://www.ice.gov/most-wanted#tab0
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

    data_list = []
    url = 'https://www.ice.gov/most-wanted#tab0'
    soup = get_soup(url)
    data_sec = soup.find_all('li', {'class': 'grid'})
    for data in data_sec:
        data_dict = {}
        fullName = ''
        image = ''
        alias = ''
        placeOfBirthCountry = ''
        gender = ''
        age = ''
        designation = ''
        height = ''
        weight = ''
        eyes = ''
        hair = ''
        distinguishMarks = ''
        wantedFor = ''
        summary = ''
        additionalInfo = ''

        try:
            fullName = data.find('div', {'class': 'mw-name'}).text.strip()
        except Exception:
            pass
        try:
            temp = data.find('div', {'class': 'mw-image'})
            image = 'https://www.ice.gov' + temp.find('img')['src']
        except Exception:
            pass
        try:
            wantedFor = data.find('div', {'class': 'mw-wantfor'}).text.strip()
        except Exception:
            pass
        try:
            link = data.find('a')['href']
            soup = get_soup(link)
            info = soup.find('div', {'class': 'mw-info-wrapper grid-col-12 desktop:grid-col-9'})
            for items in info:
                text = items.text.replace('\n', '').strip()
                if 'Alias' in text:
                    alias = text.replace('Alias', '')
                if 'Place of Birth' in text:
                    placeOfBirthCountry = text.replace('Place of Birth', '')
                if 'Gender' in text:
                    gender = text.replace('Gender', '')
                if 'Age' in text:
                    age = text.replace('Age', '')
                if 'Last Known Location' in text:
                    additionalInfo = "Last Known Location: " + text.replace('Last Known Location', '')
                if 'Occupation' in text:
                    designation = text.replace('Occupation', '')

            info2 = soup.find('div', {'class': 'mw-pd-item-1 grid-col-12 desktop:grid-col-6'})
            for items in info2:
                text = items.text.replace('\n', '').strip()
                if 'Height' in text:
                    height = text.replace('Height', '')
                if 'Weight' in text:
                    weight = text.replace('Weight', '')
                if 'Skin Tone' in text:
                    additionalInfo += ", Skin Tone: " + text.replace('Skin Tone', '')

            info3 = soup.find('div', {'class': 'mw-pd-item-2 grid-col-12 desktop:grid-col-6'})
            for items in info3:
                text = items.text.replace('\n', '').strip()
                if 'Eyes' in text:
                    eyes = text.replace('Eyes', '')
                if 'Hair' in text:
                    hair = text.replace('Hair', '')
                if 'Scars/Marks' in text:
                    distinguishMarks = text.replace('Scars/Marks', '')

        except Exception:
            pass

        if fullName:
            data_dict['fullName'] = fullName
            data_dict['image'] = image
            data_dict['category'] = 'CRIME'
            data_dict['alias'] = alias
            data_dict['age'] = age
            data_dict['gender'] = gender
            data_dict['placeOfBirthCountry'] = placeOfBirthCountry
            data_dict['designation'] = designation
            data_dict['height'] = height
            data_dict['weight'] = weight
            data_dict['eyes'] = eyes
            data_dict['hair'] = hair
            data_dict['distinguishMarks'] = distinguishMarks
            data_dict['wantedFor'] = wantedFor
            data_dict['additionalInfo'] = additionalInfo
            data_dict['summary'] = fullName + " is a Most Wanted Fugitive listed by U.S Immigration and Customs Enforcement"
            # print(data_dict)
            data_dict['UpdationFlag'] = True
            html_hash = get_hash_of_html(str(data_dict))
            data_dict['RawHtml'] = html_hash
            data_dict['LastUpdatedDev'] = last_updated_dev
            data_dict['UpdateLabelTs'] = update_label_ts

        if data_dict:
            data_list.append(data_dict)

    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    # print(data_list)
