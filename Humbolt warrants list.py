'''
Month_assigned : April
Date Submitted : 18-04-2022
Date_source_name : Humbolt warrants list
Harvesting_URL : https://humboldtgov.org/DocumentCenter/View/73312/Warrants-list-as-of-4-6-2022
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
import fitz
import io
from PIL import Image
import PyPDF2
import codecs
from googletrans import Translator

translator = Translator()


def to_json(data_list):
    hash_obj = json.dumps(data_list)
    with open('json/dictionary.json', 'w') as ts:
        ts.write(hash_obj)


# def get_soup(url):
#     res = requests.get(url)
#     soup = bs(res.text, 'html.parser')
#     return soup


def get_hash_of_html(html_string):
    hash_object = hashlib.md5(html_string.encode('utf-8'))
    hash_of_html = hash_object.hexdigest()
    return hash_of_html


def get_data(slug_name):
    data_list = []

    pdfFileObj = open(r"C:\Users\Ansh\Downloads\AllBeats_147.pdf", 'rb')
    text = ''
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    for j in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(j)
        text = text + pageObj.extractText()

    temp = text.replace('Active Felony & Bookable Misdemeanor Warrants by Beat/City', '').replace(
        'Oldest possible warrant listed on report:  4/14/2019', '').replace('All Beats', '').replace('Run Date:',
                                                                                                     '').replace(
        'Central Beat / BAYSIDE', '').replace('Central Beat / EUREKA', '').replace('Garberville Beat / BLOCKSBURG',
                                                                                   '').replace(
        'Garberville Beat / GARBERVILLE', '').replace('Garberville Beat / MIRANDA', '').replace(
        'Garberville Beat / PETROLIA', '').replace('Garberville Beat / REDWAY', '').replace(
        'Garberville Beat / SHELTER COVE', '').replace('Hoopa Beat / HOOPA', '').replace('Hoopa Beat / WILLOW CREEK',
                                                                                         '').replace(
        'North Beat / ARCATA', '').replace('North Beat / BLUE LAKE', '').replace('North Beat / ARCATA', '').replace(
        'North Beat / MCKINLEYVILLE', '').replace('North Beat / ORICK', '').replace('North Beat / TRINIDAD',
                                                                                    '').replace(
        'South Beat / ALDERPOINT', '').replace('South Beat / BRIDGEVILLE', '').replace('South Beat / CUTTEN',
                                                                                       '').replace(
        'South Beat / FORTUNA', '').replace('South Beat / KING SALMON', '').replace('South Beat / LOLETA', '').replace(
        'South Beat / RIO DELL', '').replace('South Beat / SCOTIA', '').replace('POCASANGREGALLEGOS, BRYAN ',
                                                                                '').replace(
        'MAGUIRESALVATORI, SHANNON ', '').replace('MOSELEYSTONEBARGER, KRISTINA ', '').replace(
        'Garberville Beat / HONEYDEW', '').replace('Garberville Beat / MYERS FLAT', '').replace(
        'Garberville Beat / PHILLIPSVILLE', '').replace('Garberville Beat / WEOTT', '').replace(
        'Garberville Beat / WHITETHORN', '').replace('Hoopa Beat / ORLEANS', '').replace('BROCKDONAHUE, NATESSALEI ',
                                                                                         '').replace(
        'North Beat / FIELDBROOK', '').replace('North Beat / KORBEL', '').replace('North Beat / WESTHAVEN', '').replace(
        'South Beat / CARLOTTA', '').replace('South Beat / FERNDALE', '').replace('South Beat / HYDESVILLE',
                                                                                  '').replace('South Beat / MAD RIVER',
                                                                                              '').replace(
        'South Beat / REDCREST', '').replace('Central Beat / FAIRHAVEN', '').replace('Central Beat / KNEELAND',
                                                                                     '').replace(
        'Central Beat / MANILA', '').replace('Central Beat / MYRTLETOWN', '').replace('Central Beat / SAMOA',
                                                                                      '').replace(
        'CORDEROMCCULLOUGH, ROBERT ', '')

    temp2 = temp.split('4/13/2022 8:15:04 AM')
    temp3 = []
    for i in temp2:
        temp3 = i.split('\n')
        temp4 = [i for i in temp3 if i]
        if temp4[0] == 'Page ':
            temp5 = temp4[5:-1]
        else:
            temp5 = temp4[:-1]
        # print(temp5)
        for j in range(0, len(temp5), 6):
            temp6 = temp5[j:j + 6]
            data_dict = {}
            data_dict['fullName'] = temp6[1].strip()
            data_dict['dob'] = temp6[4].replace('DOB:', '').strip()
            data_dict['category'] = 'Individual'
            data_dict['state'] = 'California'
            data_dict['country'] = 'United States'
            data_dict['importantDates'] = 'Warrant Issue Date: ' + temp6[5].replace('Issued:', '').strip()
            data_dict['additionalInfo'] = temp6[0].strip() + " " + temp6[2].strip() + " " + temp6[3].strip()
            data_dict['summary'] = temp6[1].strip() + ' is a criminal under warrant by California State, U.S'
            html_hash = get_hash_of_html(str(data_dict))
            data_dict['UpdationFlag'] = True
            data_dict['RawHtml'] = html_hash
            data_dict['LastUpdatedDev'] = last_updated_dev
            data_dict['UpdateLabelTs'] = update_label_ts
            data_list.append(data_dict)

    return data_list


if __name__ == "__main__":
    last_updated_dev = int(time.time())
    update_label_ts = int(time.time())

    data_list = get_data('add-slug-here')
    # to_json(data_list)
    print(data_list)
