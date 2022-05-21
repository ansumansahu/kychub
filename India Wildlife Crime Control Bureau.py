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


def extract_entity(data_sec, raw_html, slug_name, i):
    html_hash = get_hash_of_html(raw_html)

    if data_sec:
        data_dict = {}
        fullName = ''
        title = ''
        designation = ''
        addressLine1 = ''
        city = ''
        telephoneNos = ''
        emails = ''
        summary = ''

        try:
            ele = driver.find_element(By.XPATH,f"/html/body/form/div[3]/div[2]/div[3]/div[1]/div[3]/div[2]/div/table/tbody/tr[{i}]/td[2]").text
            fullName = " ".join(ele.split()[1:])
            title = "".join(ele.split()[0])
        except Exception:
            pass

        try:
            designation = driver.find_element(By.XPATH,f"/html/body/form/div[3]/div[2]/div[3]/div[1]/div[3]/div[2]/div/table/tbody/tr[{i}]/td[3]").text
        except Exception:
            pass

        try:
            ele = driver.find_element(By.XPATH,f"/html/body/form/div[3]/div[2]/div[3]/div[1]/div[3]/div[2]/div/table/tbody/tr[{i}]/td[4]").text.replace("&nbsp;","").strip()
            temp = "".join(ele.split()[:2])
            city = "".join(ele.split()[2:])
            addressLine1 = temp + " " + city
        except Exception:
            pass

        try:
            telephoneNos = driver.find_element(By.XPATH,f"/html/body/form/div[3]/div[2]/div[3]/div[1]/div[3]/div[2]/div/table/tbody/tr[{i}]/td[5]").text
        except Exception:
            pass

        try:
            emails = driver.find_element(By.XPATH,f"/html/body/form/div[3]/div[2]/div[3]/div[1]/div[3]/div[2]/div/table/tbody/tr[{i}]/td[6]").text.replace("[at]","@").replace("[dot]",".")
        except Exception:
            pass

        try:
            summary = title + " " + fullName + " is an officer of Wildlife Crime Control Bureau currently posted in " + city
        except Exception:
            pass

        if fullName:
            data_dict['fullName'] = fullName
            data_dict['title'] = title
            data_dict['designation'] = designation
            data_dict['addressLine1'] = addressLine1
            data_dict['city'] = city
            data_dict['telephoneNos'] = telephoneNos
            data_dict['emails'] = emails
            data_dict['summary'] = summary
            data_dict['EmployeeName'] = "Ansuman Sahu"
            data_dict['UpdationFlag'] = True
            data_dict['RawHtml'] = html_hash
            data_dict['LastUpdatedDev'] = last_updated_dev
            data_dict['UpdateLabelTs'] = update_label_ts
            # print(data_dict)

        return data_dict
    return {}


def get_data(slug_name):
    url = 'http://wccb.gov.in/Content/DirectoryofWCCBOfficers.aspx'

    data_list = []

    driver.get(url)
    time.sleep(1)

    li = driver.find_elements(By.XPATH,f"/html/body/form/div[3]/div[2]/div[3]/div[1]/div[3]/div[2]/div/table/tbody/tr")
    # print(len(li))

    for i in range(2, len(li)+2):
        try:
            data_section = driver.find_elements(By.XPATH,f"/html/body/form/div[3]/div[2]/div[3]/div[1]/div[3]/div[2]/div/table/tbody/tr[{i}]")
            for data in data_section:
                data_dict = extract_entity(data, str(data), slug_name, i)
                if data_dict:
                    data_list.append(data_dict)

        except Exception:
            pass

    # print(len(data_list))
    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    print(data_list)