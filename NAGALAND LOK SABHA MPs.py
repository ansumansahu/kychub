'''
Month_assigned : April
Date Submitted : 20-04-2022
Date_source_name : NAGALAND LOK SABHA MPs
Harvesting_URL : https://www.sarkaritel.com/states/member_of_parliament_list_lok_sabha.php?state=NL
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


def get_data(slug_name):
    last_updated_dev = int(time.time())
    update_label_ts = int(time.time())

    PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver\\chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(PATH)
    driver.maximize_window()

    data_list = []
    url = 'https://www.sarkaritel.com/states/member_of_parliament_list_lok_sabha.php?state=NL'
    driver.get(url)
    time.sleep(1)

    try:
        data_section = driver.find_elements(By.XPATH, '/html/body/div/div/div[2]/div/div[3]/div/div[2]/div[1]/div/div/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table')
        for data in data_section:
            if data:
                data_dict = {}
                fullName = ''
                designation = ''
                image = ''
                telephoneNos = ''
                politicalPartyName = ''
                constituency = ''
                additionalInfo = ''

                try:
                    image = data.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                except Exception:
                    pass

                text = data.text
                for line in text.split('\n'):
                    # print(line)
                    if '[Profile]' in line:
                        fullName = line.replace('[Profile]', '').strip()
                        # print(fullName)
                    if 'Constituency Address :' in line:
                        additionalInfo = line.replace(',', '').replace('-', '').strip()
                    if 'Fax :' in line:
                        additionalInfo += ' ,' + line.strip()
                    if 'Delhi Address :' in line:
                        additionalInfo += ' ,' + line.replace(',', '').replace('-', '').strip()
                    if 'Telephone :' in line:
                        telephoneNos += " " + line.replace('Telephone :', '').strip()
                    if 'Party :' in line:
                        politicalPartyName = line.replace('Party :', '').strip()
                    if 'Constituency / State :' in line:
                        constituency = line.replace('Constituency / State :', '').replace('(Nagaland)', '').strip()

                summary = fullName + " is a Member Of Parliament (Lok Sabha) of Nagaland and also a member of " + politicalPartyName + " political party"

                if fullName:
                    data_dict['fullName'] = fullName
                    data_dict['image'] = image
                    data_dict['category'] = 'Individual'
                    data_dict['designation'] = 'Member Of Parliament'
                    data_dict['telephoneNos'] = telephoneNos
                    data_dict['politicalPartyName'] = politicalPartyName
                    data_dict['constituency'] = constituency
                    data_dict['state'] = 'Nagaland'
                    data_dict['country'] = 'India'
                    data_dict['additionalInfo'] = additionalInfo
                    data_dict['summary'] = summary
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

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    print(data_list)
