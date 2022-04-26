'''
Month_assigned : April
Date Submitted : 25-04-2022
Date_source_name : Los Angeles Police Most Wanted
Harvesting_URL : https://www.lapdonline.org/lapd-most-wanted/
Data_Extractor : Ansuman Sahu
'''

import re
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

    url = 'https://www.lapdonline.org/lapd-most-wanted/'
    soup = get_soup(url)

    data_secs = soup.find_all('div', {'class': 'col-6 col-md-3 col-lg-3 col-xl-2'})
    # print(len(data_secs))
    for data_sec in data_secs:
        if data_sec:
            data_dict = {}
            fullName = ''
            image = ''
            dob = ''
            race = ''
            gender = ''
            height = ''
            weight = ''
            hair = ''
            eyes = ''
            wantedFor = ''
            distinguishMarks = ''
            additionalInfo = ''

            try:
                fullName = data_sec.find('div', {'class': 'card-inner'}).text.strip()
            except Exception:
                pass

            try:
                image = data_sec.find('img')['src']
            except Exception:
                pass

            try:
                link = data_sec.find('a')['href']
                soup = get_soup(link)
                data = soup.find('div', {'class': 'col-12 col-md-9 col-xl-8 ml-lg-auto wow fadeInUp'})
                try:
                    additionalInfo = data.text.split('Details')[1].strip()
                    # print(additionalInfo)
                except Exception:
                    pass
                try:
                    info_list = data.find('ul', {'class': 'list-unstyled'})
                    lines = info_list.find_all('li')
                    for line in lines:
                        temp = line.text
                        if 'Wanted For:' in temp:
                            wantedFor = temp.replace('Wanted For:', '').strip()
                        if 'Sex:' in temp:
                            gender = temp.replace('Sex:', '').strip()
                        if 'Descent:' in temp:
                            race = temp.replace('Descent:', '').strip()
                        if 'Height:' in temp:
                            height = temp.replace('Height:', '').strip()
                        if 'Weight:' in temp:
                            weight = temp.replace('Weight:', '').strip()
                        if 'Hair:' in temp:
                            hair = temp.replace('Hair:', '').strip()
                        if 'Eyes:' in temp:
                            eyes = temp.replace('Eyes:', '').strip()
                        if 'Date of Birth:' in temp:
                            dob = temp.replace('Date of Birth:', '').strip()
                        if 'Oddities:' in temp:
                            distinguishMarks = temp.replace('Oddities:', '').strip()
                        if 'DR#:' in temp:
                            additionalInfo += " ," + temp.strip()
                        if 'Weapon:' in temp:
                            additionalInfo += " ," + temp.strip()

                except Exception:
                    pass

            except Exception:
                pass

            if fullName:
                data_dict['fullName'] = fullName
                data_dict['image'] = image
                data_dict['gender'] = gender
                data_dict['dob'] = dob
                data_dict['height'] = height
                data_dict['weight'] = weight
                data_dict['race'] = race
                data_dict['eyes'] = eyes
                data_dict['hair'] = hair
                data_dict['distinguishMarks'] = distinguishMarks
                data_dict['wantedFor'] = wantedFor
                data_dict['category'] = 'CRIME'
                data_dict['additionalInfo'] = additionalInfo
                data_dict['summary'] = fullName + " is a Most Wanted individual from the Greater Los Angeles Area, California, U.S"
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
    data_list = get_data('slug')
    # to_json(data_list)
    # print(data_list)
