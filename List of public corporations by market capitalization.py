import PyPDF2
from bs4 import BeautifulSoup as bs
import time
import requests
import hashlib
import googletrans
from googletrans import Translator
import json
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
from urllib.request import urlopen as uReq
# from ..general_utility import get_hash_of_html
# from ..s3_upload import hash_check


def get_hash_of_html(html_string):
    hash_object = hashlib.md5(html_string.encode('utf-8'))
    hash_of_html = hash_object.hexdigest()
    return hash_of_html


def get_soup(url):
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')
    return soup


def to_json(entity):
    hash_obj = json.dumps(entity)
    with open("dictionary.json", "w") as ts:
        ts.write(hash_obj)


def extract_entity(data, raw_html, slug,i,l):
    last_updated_dev = int(time.time())
    update_label_ts = int(time.time())

    html_hash = get_hash_of_html(str(raw_html))

    data_dict = {}
    if data:
        try:
            companyInfo = ''
            temp = data.find_all('td')
            if i < l - 13:
                temp1 = temp[2].a['href']
                link = 'https://en.wikipedia.org/' + temp1
                data_dict['fullName'] = temp[2].a.text
                data_dict['links'] = link
            else:
                temp1 = temp[1].a['href']
                link = 'https://en.wikipedia.org/' + temp1
                data_dict['fullName'] = temp[1].text.strip()
                data_dict['links'] = link

            soup = get_soup(link)
            data = soup.find_all('p')
            i = 0
            for data1 in data:
                i = i+1
            summary = data[1].text.strip()
            temp = soup.find_all('td', {'class': 'infobox-image logo'})
            try:
                img = temp[1].img['src']
                img = 'https://'+img
                data_dict['image'] = img
            except Exception:
                pass
            data_dict['category'] = 'Organisation'
            try:
                temp = soup.find('table', {'class': 'infobox vcard'})
                temp1 = temp.find_all('tr')
                for data in temp1:
                    data1 = data.text
                    try:
                        type_ele = data1.split('Type')
                        companyInfo = 'Type: ' + type_ele[1].strip()
                    except Exception:
                        pass
                    try:
                        ele = data1.split('Founded')
                        companyInfo += ', Founded: ' + ele[1].strip().replace('\xa0', ' ')
                    except Exception:
                        pass
                    try:
                        ele = data1.split('Traded as')
                        companyInfo += ', Traded as: ' + ele[1].replace('\xa0', ' ').replace('component', ",")
                    except Exception:
                        pass
                    try:
                        ele = data1.split('ISIN')
                        companyInfo += ', ISIN: ' + ele[1]
                    except Exception:
                        pass
                    try:
                        ele = data1.split('Industry')
                        companyInfo += ', Industry: ' + ele[1].strip()
                    except Exception:
                        pass
                    try:
                        ele = data1.split('Headquarters')
                        companyInfo += ', Headquarters: ' + ele[1]
                    except Exception:
                        pass
                    try:
                        ele = data1.split('Key people')
                        companyInfo += ', Key people: ' + ele[1]
                    except Exception:
                        pass
                    try:
                        ele = data1.split('Products')
                        companyInfo += ', Products: ' + ele[1]
                    except Exception:
                        pass
                    try:
                        ele = data1.split('Services')
                        companyInfo += ', Services: ' + ele[1]
                    except Exception:
                        pass
                    try:
                        ele = data1.split('Revenue')
                        companyInfo += ', Revenue: ' + ele[1].replace('\xa0', ' ')
                    except Exception:
                        pass
                    try:
                        ele = data1.split('Operating income')
                        companyInfo += ', Operating income: ' + ele[1].replace('\xa0', ' ')
                    except Exception:
                        pass
                    try:
                        ele = data1.split('Net income')
                        companyInfo += ', Net income: ' + ele[1].replace('\xa0', ' ')
                    except Exception:
                        pass
                    try:
                        ele = data1.split('Total assets')
                        companyInfo += ', Total assets: ' + ele[1].replace('\xa0', ' ')
                    except Exception:
                        pass
                    try:
                        ele = data1.split('Total equity')
                        companyInfo += ', Total equity: ' + ele[1].replace('\xa0', ' ')
                    except Exception:
                        pass
                    try:
                        ele = data1.split('Number of employees')
                        companyInfo += ', Number of employees: ' + ele[1].replace('\xa0', ' ')
                    except Exception:
                        pass
            except Exception:
                pass

            data_dict['companyInfo'] = companyInfo
            data_dict['summary'] = summary
            data_dict['UpdationFlag'] = True
            data_dict['RawHtml'] = html_hash
            data_dict['LastUpdatedDev'] = last_updated_dev
            data_dict['UpdateLabelTs'] = update_label_ts

        except Exception:
            pass

    return data_dict


def get_data(slug):
    url = 'https://en.wikipedia.org/wiki/List_of_public_corporations_by_market_capitalization'
    soup = get_soup(url)

    data_a = soup.find_all('table')
    l = len(data_a)

    data_list = []
    i = 0
    for data in data_a:
        if 0 < i < len(data_a) - 4:
            temp = data.find_all('tr')
            for data1 in temp:
                data_dict = extract_entity(data1, str(data1), slug, i, l)
                if data_dict:
                    print(data_dict)
                    data_list.append(data_dict)
        i = i+1

    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    print(data_list)
    # to_json(data_list)
