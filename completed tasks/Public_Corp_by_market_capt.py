import PyPDF2
from bs4 import BeautifulSoup as bs
import time
import requests
import hashlib
import googletrans
from googletrans import Translator

last_updated_dev = int(time.time())
update_label_ts = int(time.time())
import json
from googletrans import Translator

translator = Translator()

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
from urllib.request import urlopen as uReq


# from ..general_utility import get_hash_of_html
# from ..s3_upload import hash_check


def to_json(data_list):
    pass


def get_hash_of_html(html_string):
    hash_object = hashlib.md5(html_string.encode('utf-8'))
    hash_of_html = hash_object.hexdigest()
    return hash_of_html


def get_soup(url):
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')
    return soup


def lang_conversion(text):
    return translator.translate(text).text


'''
def to_json(entity):
    hash_obj = json.dumps(entity)
    with open("dictionary.json", "w") as ts:
        ts.write(hash_obj)

'''
def extract_entity(data, raw_html, slug,i,l):
    html_hash = get_hash_of_html(str(raw_html))

    if data:
        try:
            data_dict = {}
            temp = data.find_all('td')
            if i < l - 13:
                temp1 = temp[2].a['href']
                link = 'https://en.wikipedia.org/' + temp1
                print(temp[2].a.text, link)
                data_dict['name'] = temp[2].a.text
                data_dict['link'] = link
            else:
                temp1 = temp[1].a['href']
                link = 'https://en.wikipedia.org/' + temp1
                print(temp[1].text, link)
                data_dict['name'] = temp[1].text.strip()
                data_dict['link'] = link

            soup = get_soup(link)
            data = soup.find_all('p')
            i=0
            for data1 in data:
                i=i+1
            summary = data[1].text.strip()
            print('summary=', summary)
            data_dict['summary'] = summary
            temp = soup.find_all('td',{'class':'infobox-image logo'})
            try:
                img = temp[1].img['src']
                img = 'https://'+img
                print(img)
                data_dict['image'] = img
            except Exception:
                pass
            try:
                temp = soup.find('table',{'class':'infobox vcard'})
                temp1 = temp.find_all('tr')
                for data in temp1:
                    data1=data.text
                    try:
                        type_ele=data1.split('Type')
                        print("Type : " + type_ele[1])
                        data_dict['Type'] = type_ele[1].strip()
                    except Exception:
                        pass
                    try:
                        ele=data1.split('Founded')
                        print("years : " + ele[1])
                        data_dict['years'] = ele[1].strip().replace('\xa0', ' ')
                    except Exception:
                        pass
                    try:
                        ele = data1.split('Traded as')
                        print("Traded As : " + ele[1])
                        data_dict['Traded as'] = ele[1].replace('\xa0', ' ').replace('component', ",")
                    except Exception:
                        pass
                    try:
                        ele=data1.split('ISIN')
                        print("ISIN : " + ele[1])
                        data_dict['ISIN'] = ele[1]
                    except Exception:
                        pass
                    try:
                        ele=data1.split('Industry')
                        print("entity : " + ele[1])
                        data_dict['entity'] = ele[1].strip()
                    except Exception:
                        pass
                    try:
                        ele=data1.split('Headquarters')
                        print("Headquarters in " + ele[1])
                        data_dict['Headquarters'] = ele[1]
                    except Exception:
                        pass
                    try:
                        ele=data1.split('Key people')
                        data_dict['Key people'] = ele[1]
                    except Exception:
                        pass
                    try:
                        ele=data1.split('Products')
                        print("Products : "+ ele[1])
                        data_dict['Products'] = ele[1]
                    except Exception:
                        pass
                    try:
                        ele=data1.split('Services')
                        print("Services : " + ele[1])
                        data_dict['Services'] = ele[1]
                    except Exception:
                        pass
                    try:
                        ele=data1.split('Revenue')
                        ele = data1.split('Revenue')
                        data_dict['Revenue'] = ele[1].replace('\xa0', ' ')
                    except Exception:
                        pass
                    try:
                        ele=data1.split('Operating income')
                        print("Operating income : " + ele[1])
                        data_dict['Operating income'] = ele[1].replace('\xa0', ' ')
                    except Exception:
                        pass
                    try:
                        ele=data1.split('Net income')
                        print("Net income : " + ele[1])
                        data_dict['Net income'] = ele[1].replace('\xa0', ' ')
                    except Exception:
                        pass
                    try:
                        ele=data1.split('Total assets')
                        print("Total assets : " + ele[1])
                        data_dict['Total assets'] = ele[1].replace('\xa0', ' ')
                    except Exception:
                        pass
                    try:
                        ele=data1.split('Total equity')
                        print("Total equity : " + ele[1])
                        data_dict['Total equity'] = ele[1].replace('\xa0', ' ')
                    except Exception:
                        pass
                    try:
                        ele=data1.split('Number of employees')
                        print("Number of employees : " + ele[1])
                        data_dict['Number of employees'] = ele[1].replace('\xa0', ' ')
                    except Exception:
                        pass
            except Exception:
                pass

            data_dict['EmployeeName'] = "Ansuman Sahu"
            data_dict['UpdationFlag'] = False
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
    l=len(data_a)

    data_list = []
    i=0
    for data in data_a:
        if 0 < i < len(data_a)-4:
            temp = data.find_all('tr')
            for data1 in temp:
                data_dict = extract_entity(data1, str(data1), slug,i,l)
                if data_dict:
                    data_list.append(data_dict)
        i=i+1

    return data_list

if __name__ =="__main__":
    data_list = get_data('add-slug-here')
    print(data_list)
    to_json(data_list)
    # print(data_list)

