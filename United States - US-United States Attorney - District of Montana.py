'''
Month_assigned : May
Date Submitted : 10-05-2022
Date_source_name : United States - US-United States Attorney - District of Montana
Harvesting_URL : https://www.mtd.uscourts.gov/judges
Data_Extractor : Ansuman Sahu
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
    url = 'https://www.mtd.uscourts.gov/judges'
    soup = get_soup(url)

    try:
        data_sec = soup.find('div', {'class': 'field__item even'})
        li = data_sec.find_all('li')
        for item in li:
            data_dict = {}
            fullName = ''
            designation = ''
            image = ''
            fullAddress = ''
            educationInfo = ''
            additionalInfo = ''

            try:
                temp = item.text.strip()
                fullName = temp.split(",")[0].strip()
                designation = temp.split(",")[1].strip()
            except Exception:
                pass

            try:
                link = "https://www.mtd.uscourts.gov" + item.find('a')['href']
                soup = get_soup(link)

                image = "https://www.mtd.uscourts.gov" + (soup.find_all('img'))[1]['src']

                text = soup.find('div', {'class': 'field__item even'}).text.replace(f'{fullName}', '').replace('\xa0', '').replace('\t', '').replace('\ufeff', '').replace('The Honorable', '')
                info_list = [i for i in text.split("\n") if i]

                fullAddress = text.split('Chambers')[0].strip().replace('\n', ' ')

                for line in info_list:
                    if 'Chambers' in line:
                        if ':' in line:
                            additionalInfo = line.strip()
                        else:
                            additionalInfo = 'Chambers: ' + line.replace('Chambers', '').strip()
                    if 'EDUCATION' in line:
                        educationInfo = line.replace('EDUCATION:', '').strip()
                    if 'MILITARY SERVICE' in line:
                        additionalInfo += "; " + line.strip()
                    if 'CAREER RECORD' in line:
                        additionalInfo += "; " + line.strip()
                    if 'MEMBERSHIPS' in line:
                        additionalInfo += "; " + line.strip()

            except Exception:
                pass

            if fullName:
                data_dict['fullName'] = fullName
                data_dict['designation'] = designation
                data_dict['title'] = 'Honorable'
                data_dict['category'] = 'SIP'
                data_dict['image'] = image
                data_dict['fullAddress'] = fullAddress
                data_dict['educationInfo'] = educationInfo
                data_dict['additionalInfo'] = additionalInfo
                data_dict['summary'] = fullName + "is a United States Court Judge of Montana District"
                # print(data_dict)
                html_hash = get_hash_of_html(str(data_dict))
                data_dict['UpdationFlag'] = True
                data_dict['RawHtml'] = html_hash
                data_dict['LastUpdatedDev'] = last_updated_dev
                data_dict['UpdateLabelTs'] = update_label_ts

            if data_dict:
                data_list.append(data_dict)

    except Exception:
        pass

    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    # print(data_list)
