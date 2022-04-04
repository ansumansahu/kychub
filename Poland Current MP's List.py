'''
Month_assigned : March
Date Submitted : 01-04-2022
Date_source_name : Poland Current MP's List
Data_source_URL : https://www.sejm.gov.pl/poslowie/lista6.htm#B
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
from googletrans import Translator
translator = Translator()

last_updated_dev = int(time.time())
update_label_ts = int(time.time())

options = webdriver.ChromeOptions()
prefs = {
    "translate_whitelists": {"pl": "en"},
    "translate": {"enabled": "true"}
}
options.add_experimental_option("prefs", prefs)

PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver\\chromedriver.exe"
driver = webdriver.Chrome(options=options, executable_path=PATH)
# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(PATH)
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


def lang_conversion(text):
    return translator.translate(text).text


def get_data(slug_name):
    url = 'https://www.sejm.gov.pl/poslowie/lista6.htm#B'

    data_list = []

    driver.get(url)
    time.sleep(3)

    li = driver.find_elements(By.CSS_SELECTOR, 'a.a1n')
    print(len(li))

    driver.find_element(By.XPATH, '/html/body/center/table/tbody/tr[3]/td/table[2]/tbody/tr/td[2]/a[2]').click() #start from 2
    time.sleep(1)

    data_dict = {}
    fullName = ''
    image = ''
    careerInfoStartDate = ''
    politicalPartyName = ''
    constituency = ''
    dob = ''
    placeOfBirthCity = ''
    maritalStatus = ''
    educationInfo = ''
    summary = ''

    try:
        fullName = driver.find_element(By.XPATH, "/html/body/center/table[1]/tbody/tr[3]/td[2]/p[1]").text
    except Exception:
        pass

    try:
        image = driver.find_element(By.XPATH, "/html/body/center/table[1]/tbody/tr[3]/td[1]/img").get_attribute('src')
    except Exception:
        pass

    try:
        temp = driver.find_element(By.XPATH, "/html/body/center/table[1]/tbody/tr[3]/td[2]/p[2]").text
        careerInfoStartDate = temp.split(':')[1].replace('"', '').strip()
    except Exception:
        pass

    try:
        temp = driver.find_element(By.XPATH, "/html/body/center/table[1]/tbody/tr[3]/td[2]/li[1]").text
        politicalPartyName = temp.split(':')[1].replace('"', '').strip()
    except Exception:
        pass

    try:
        temp = driver.find_element(By.XPATH, "/html/body/center/table[1]/tbody/tr[3]/td[2]/li[2]").text
        constituency = temp.split(':')[1].replace('"', '').strip()
    except Exception:
        pass

    try:
        temp = driver.find_element(By.XPATH, "/html/body/center/table[3]/tbody/tr/td/p").text
        temp2 = temp.split('\n')
        temp3 = temp2[0].split(':')[1].replace('"', '').strip()
        placeOfBirthCity = temp3.split(',')[-1]
        dob = "".join(temp3.split(',')[:-1])
        maritalStatus = temp2[1].split(':')[1].replace('"', '').strip()
        educationInfo = temp2[3].split(':')[1].replace('"', '').strip()

    except Exception:
        pass

    try:
        summary = fullName + " is a MP and also a member of " + politicalPartyName + " political party in Poland"
    except Exception:
        pass

    if fullName:
        data_dict['fullName'] = fullName
        data_dict['image'] = image
        data_dict['careerInfoStartDate'] = careerInfoStartDate
        data_dict['politicalPartyName'] = politicalPartyName
        data_dict['constituency'] = constituency
        data_dict['dob'] = dob
        data_dict['placeOfBirthCity'] = placeOfBirthCity
        data_dict['maritalStatus'] = maritalStatus
        data_dict['educationInfo'] = educationInfo
        data_dict['summary'] = summary
        html_hash = get_hash_of_html(str(data_dict))
        # data_dict['EmployeeName'] = "Ansuman Sahu"
        data_dict['UpdationFlag'] = True
        data_dict['RawHtml'] = html_hash
        data_dict['LastUpdatedDev'] = last_updated_dev
        data_dict['UpdateLabelTs'] = update_label_ts
        data_list.append(data_dict)

    # for i in range(1, 6): #for test
    for i in range(len(li)):
        try:
            driver.find_element(By.XPATH, "/html/body/center/table[1]/tbody/tr[3]/td[2]/a[1]/img").click()
            time.sleep(2)
            data_dict = {}
            fullName = ''
            image = ''
            careerInfoStartDate = ''
            politicalPartyName = ''
            constituency = ''
            dob = ''
            placeOfBirthCity = ''
            maritalStatus = ''
            educationInfo = ''
            summary = ''

            try:
                fullName = driver.find_element(By.XPATH,"/html/body/center/table[1]/tbody/tr[3]/td[2]/p[1]").text
            except Exception:
                pass

            try:
                image = driver.find_element(By.XPATH,"/html/body/center/table[1]/tbody/tr[3]/td[1]/img").get_attribute('src')
            except Exception:
                pass

            try:
                temp = driver.find_element(By.XPATH,"/html/body/center/table[1]/tbody/tr[3]/td[2]/p[2]").text
                careerInfoStartDate = temp.split(':')[1].replace('"', '').strip()
            except Exception:
                pass

            try:
                temp = driver.find_element(By.XPATH,"/html/body/center/table[1]/tbody/tr[3]/td[2]/li[1]").text
                politicalPartyName = temp.split(':')[1].replace('"', '').strip()
            except Exception:
                pass

            try:
                temp = driver.find_element(By.XPATH,"/html/body/center/table[1]/tbody/tr[3]/td[2]/li[2]").text
                constituency = temp.split(':')[1].replace('"', '').strip()
            except Exception:
                pass

            try:
                temp = driver.find_element(By.XPATH, "/html/body/center/table[3]/tbody/tr/td/p").text
                temp2 = temp.split('\n')
                temp3 = temp2[0].split(':')[1].replace('"', '').strip()
                placeOfBirthCity = temp3.split(',')[-1].strip()
                dob = "".join(temp3.split(',')[:-1]).strip()
                maritalStatus = temp2[1].split(':')[1].replace('"', '').strip()
                educationInfo = temp2[3].split(':')[1].replace('"', '').strip()

            except Exception:
                pass

            try:
                summary = fullName + " is a MP and also a member of " + politicalPartyName + " political party in Poland"
            except Exception:
                pass

            if fullName:
                data_dict['fullName'] = fullName
                data_dict['image'] = image
                data_dict['careerInfoStartDate'] = careerInfoStartDate
                data_dict['politicalPartyName'] = politicalPartyName
                data_dict['constituency'] = constituency
                data_dict['dob'] = dob
                data_dict['placeOfBirthCity'] = placeOfBirthCity
                data_dict['maritalStatus'] = maritalStatus
                data_dict['educationInfo'] = educationInfo
                data_dict['summary'] = summary
                html_hash = get_hash_of_html(str(data_dict))
                data_dict['UpdationFlag'] = True
                data_dict['RawHtml'] = html_hash
                data_dict['LastUpdatedDev'] = last_updated_dev
                data_dict['UpdateLabelTs'] = update_label_ts
                data_list.append(data_dict)

        except Exception:
            pass

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    print(data_list)
