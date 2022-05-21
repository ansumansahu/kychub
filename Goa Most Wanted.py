'''
Month_assigned : April
Date Submitted : 05-04-2022
Date_source_name : Goa Most Wanted
Harvesting_URL : https://citizen.goapolice.gov.in/documents/10184/1795805/wanted1.pdf/fc9567ef-0cb5-40fd-9864-d1a36919205b
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


def lang_conversion(text):
    return translator.translate(text).text


last_updated_dev = int(time.time())
update_label_ts = int(time.time())

# options = webdriver.ChromeOptions()
# prefs = {
#     "translate_whitelists": {"ar": "en"},
#     "translate": {"enabled": "true"}
# }
# options.add_experimental_option("prefs", prefs)

# PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver\\chromedriver.exe"
# # driver = webdriver.Chrome(options=options, executable_path=PATH)
# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(PATH)
# driver.maximize_window()


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

    file = "C:/Users/Ansh/Downloads/wanted1.pdf"
    pdf_file = fitz.open(file)

    image = []

    for page_index in range(len(pdf_file)):
        # get the page itself
        page = pdf_file[page_index]
        image_list = page.getImageList()

        # printing number of images found in this page
        # if image_list:
        #     print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        # else:
        #     print("[!] No images found on page", page_index)
        for image_index, img in enumerate(page.getImageList(), start=1):
            # get the XREF of the image
            xref = img[0]
            # extract the image bytes
            base_image = pdf_file.extractImage(xref)
            image_bytes = base_image["image"]
            # get the image extension
            image_ext = base_image["ext"]
            image_data = image_bytes
            image_temp = Image.open(io.BytesIO(image_data))
            image.append(image_temp)

    pdfFileObj = open(r"C:\Users\Ansh\Downloads\wanted1.pdf", 'rb')
    text = ''
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    for j in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(j)
        text = text+pageObj.extractText()

    temp = [i for i in (text.split('W34IPC')[1]).split('English') if 'Age' in i]
    fullName = []
    age = []
    languagesKnown = []
    for i in temp:
        temp2 = i.split('Age')
        fullName.append(temp2[0].strip())
        temp3 = temp2[1].split('Language')
        age.append(temp3[0].strip())
        temp4 = temp3[1].split('Language')
        languagesKnown.append(temp4[0].replace(':', '').replace('/', ', English').strip())

    for i in range(len(fullName)):
        data_dict = {}
        data_dict['fullName'] = fullName[i]
        data_dict['age'] = age[i]
        data_dict['image'] = image[i]
        data_dict['category'] = 'Individual'
        data_dict['languagesKnown'] = languagesKnown[i]
        data_dict['country'] = 'India'
        data_dict['summary'] = fullName[i] + ' is a Most Wanted criminal by Goa Police'
        # print(data_dict)
        html_hash = get_hash_of_html(str(data_dict))
        data_dict['UpdationFlag'] = True
        data_dict['RawHtml'] = html_hash
        data_dict['LastUpdatedDev'] = last_updated_dev
        data_dict['UpdateLabelTs'] = update_label_ts
        data_list.append(data_dict)

    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    print(data_list)
