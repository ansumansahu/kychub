'''
Month_assigned : March
Date Submitted : 30-03-2022
Date_source_name : FCA (UK) Unauthorised Firms and Individuals List
Data_source_URL : https://www.fca.org.uk/consumers/unauthorised-firms-individuals#list
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

last_updated_dev = int(time.time())
update_label_ts = int(time.time())

PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver\\chromedriver.exe"
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(PATH)
driver.maximize_window()


# def to_json(data_list):
#     hash_obj = json.dumps(data_list)
#     with open('json/dictionary.json', 'w') as ts:
#         ts.write(hash_obj)


def get_hash_of_html(html_string):
    hash_object = hashlib.md5(html_string.encode('utf-8'))
    hash_of_html = hash_object.hexdigest()
    return hash_of_html


def get_soup(url):
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')
    return soup


def extract_entity(data_sec, raw_html, slug_name):
    html_hash = get_hash_of_html(raw_html)

    if data_sec:
        data_dict = {}
        name = ''
        importantDates = ''
        phone = ''
        email = ''
        address = ''
        add_info = ''
        alias = ''
        summary = ''
        mobile = ''
        website = ''

        try:
            name = data_sec.find_all('td')[0].text
            if "new" in str(name):
                name = str(name).replace("new", "").strip()[:-2].strip()
            if "updated" in str(name):
                name = str(name).replace("updated", "").strip()[:-2].strip()
            if "/" in str(name):
                alias = name.split("/", 1)[-1].strip()
                if "/" in alias:
                    alias = alias.replace("/", ";").strip()
                name = name.split("/")[0].strip()
        except Exception:
            pass

        try:
            link = "https://www.fca.org.uk" + data_sec.find('a')['href']
            soup = get_soup(link)

            try:
                add_info += "Type: " + soup.find('span', {'class': 'type'}).text.strip() + "; "
                importantDates += soup.find('span', {'class': 'pubdate'}).text.strip() + "; "
                importantDates += soup.find('span', {'class': 'pubdate latest'}).text.strip()
            except Exception:
                pass

            try:
                driver.get(link)
                time.sleep(0.15)
                temp = driver.find_element(By.CSS_SELECTOR, 'div.node-content__wrapper.node-content__wrapper--border').text.strip()

                if "\n" in temp:
                    arr = temp.split("\n")
                    for ele in arr:
                        if ele.strip():
                            if "Address" in ele:
                                address += ele.split(":")[-1].strip()
                            if "Mobile" in ele:
                                mobile += ele.split(":")[-1].strip() + ", "
                            if "Telephone" in ele:
                                phone += ele.split(":")[-1].strip() + ", "
                            if "Email" in ele:
                                email += ele.split(":")[-1].strip() + ", "
                            if "Email" in ele:
                                website += ele.split(":")[-1].strip() + ", "

                if phone:
                    if "," in phone:
                        phone = phone.replace(",", ";").strip()

            except Exception:
                pass

        except Exception:
            pass

        try:
            if name:
                summary = name.strip() + " is an Unauthorized firms listed by Financial Conduct Authority (FCA), UK."
        except Exception:
            pass

        if name:
            data_dict['fullName'] = name.strip()
            data_dict['alias'] = alias.strip()
            data_dict['importantDates'] = importantDates.replace("\t", "").strip()
            data_dict['fullAddress'] = address.strip()
            data_dict['telephoneNos'] = phone.strip()[:-1]
            data_dict['mobileNos'] = mobile.strip()[:-1]
            data_dict['emails'] = email.strip()[:-1]
            data_dict['website'] = website.strip()[:-1]
            data_dict['additionalInfo'] = add_info.strip()
            data_dict['summary'] = summary.strip()
            print(data_dict)
            data_dict['EmployeeName'] = "Ansuman Sahu"
            data_dict['UpdationFlag'] = True
            data_dict['RawHtml'] = html_hash
            data_dict['LastUpdatedDev'] = last_updated_dev
            data_dict['UpdateLabelTs'] = update_label_ts

        return data_dict
    return {}


def get_data(slug_name):
    data_list = []

    url = 'https://www.fca.org.uk/consumers/unauthorised-firms-individuals?items_per_page=25&title_field_value=&page=0'
    driver.get(url)
    soup = get_soup(url)
    time.sleep(0.15)

    temp = soup.find('div', {'class': 'view-header'}).text.strip()
    li = int(temp.replace("Displaying 1 - 25 of", '').strip())//25

    for i in range(li+1):
        print(i)
        url = f'https://www.fca.org.uk/consumers/unauthorised-firms-individuals?items_per_page=25&title_field_value=&page={i}'
        soup = get_soup(url)
        driver.get(url)
        time.sleep(0.15)
        data_div = soup.find('table', {'class': 'table table-striped cols-3'})
        data_secs = data_div.find_all('tr')

        for j in range(1, len(data_secs)):
            data_sec = data_secs[j]
            data_dict = extract_entity(data_sec, str(data_sec), slug_name)
            if data_dict:
                data_list.append(data_dict)

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    print(data_list)
    print(len(data_list))

