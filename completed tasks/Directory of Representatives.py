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


# def get_soup(url):
#     res = requests.get(url)
#     soup = bs(res.text, 'html.parser')
#     return soup


def get_hash_of_html(html_string):
    hash_object = hashlib.md5(html_string.encode('utf-8'))
    hash_of_html = hash_object.hexdigest()
    return hash_of_html


def extract_entity(data_sec, raw_html, slug_name):
    html_hash = get_hash_of_html(raw_html)

    if data_sec:
        data_dict = {}
        name = ''
        website = ''
        State = ''
        district = ''
        politicalParty = ''
        officeRoom = ''
        telephoneNos = ''
        add_info = ''
        summary = ''

        try:
            ele = data_sec.find_element(By.CSS_SELECTOR,'td.views-field.views-field-value-1.views-field-value-2').text.replace("(link is external)","").replace(",","")
            firstname = ele.split()[1]
            lastname = ele.split()[0]
            name = firstname + " " + lastname
        except Exception:
            pass

        try:
            temp1 = data_sec.find_element(By.CSS_SELECTOR,'td.views-field.views-field-value-1.views-field-value-2 > a')
            website = temp1.get_attribute('href')
        except Exception:
            pass

        try:
            ele = data_sec.find_element(By.CSS_SELECTOR,'td.views-field.views-field-value-3.views-field-value-4').text
            district = ele.split()[-1]
            State = " ".join(ele.split()[:-1])
        except Exception:
            pass

        try:
            politicalParty = data_sec.find_element(By.CSS_SELECTOR,'td.views-field.views-field-value-6').text
        except Exception:
            pass

        try:
            temp = data_sec.find_element(By.CSS_SELECTOR,'td.views-field.views-field-value-7').text
            if str(temp.split()[-1]) == "RHOB":
                officeRoom = temp.replace("RHOB", "Rayburn House Office Building")
            if str(temp.split()[-1]) == "LHOB":
                officeRoom = temp.replace("LHOB", "Longworth House Office Building")
            if str(temp.split()[-1]) == "CHOB":
                officeRoom = temp.replace("CHOB", "Cannon House Office Building")
        except Exception:
            pass

        try:
            telephoneNos = data_sec.find_element(By.CSS_SELECTOR,'td.views-field.views-field-value-9').text
        except Exception:
            pass

        try:
            temp = data_sec.find_element(By.CSS_SELECTOR,'td.views-field.views-field-markup').text.replace("\n",", ")
            add_info = "Committee Assignment: " + temp
        except Exception:
            pass

        try:
            summary = name + " currently represents " + State +"’s " + district + " Congressional District in the U.S. House of Representatives"
        except Exception:
            pass

        if name:
            data_dict['fullName'] = name
            data_dict['website'] = website
            data_dict['state'] = State
            data_dict['district'] = district
            data_dict['politicalParty'] = politicalParty
            data_dict['officeRoom'] = officeRoom
            data_dict['telephoneNos'] = telephoneNos
            data_dict['additionalInfo'] = add_info
            data_dict['summary'] = summary
            data_dict['EmployeeName'] = "Ansuman Sahu"
            data_dict['UpdationFlag'] = False
            data_dict['RawHtml'] = html_hash
            data_dict['LastUpdatedDev'] = last_updated_dev
            data_dict['UpdateLabelTs'] = update_label_ts

        return data_dict
    return {}


def get_data(slug_name):
    url = 'https://www.house.gov/representatives#state-alabama'

    data_list = []

    driver.get(url)
    time.sleep(1)

    driver.find_element(By.XPATH,"/html/body/div[2]/div/div[2]/section/div/div[2]/div/div/section[2]/div/ul/li[2]/a").click()
    time.sleep(1)

    li = driver.find_elements(By.XPATH,f"/html/body/div[2]/div/div[2]/section/div/div[2]/div/div/div/section[2]/div/div/div[2]/table")

    for i in range(1, len(li)+1):
        li2 = driver.find_elements(By.XPATH,f"/html/body/div[2]/div/div[2]/section/div/div[2]/div/div/div/section[2]/div/div/div[2]/table[{i}]/tbody/tr")

        for j in range(1, len(li2)+1):
            try:
                data_section = driver.find_elements(By.XPATH,f"/html/body/div[2]/div/div[2]/section/div/div[2]/div/div/div/section[2]/div/div/div[2]/table[{i}]/tbody/tr[{j}]")
                for data in data_section:
                    data_dict = extract_entity(data, str(data), slug_name)
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