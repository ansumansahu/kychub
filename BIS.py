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
driver = webdriver.Chrome(executable_path=PATH)
options = webdriver.ChromeOptions()
driver.maximize_window()
'''
def to_json(entity):
    hash_obj = json.dumps(entity)
    with open("dictionary.json", "w") as ts:
        ts.write(hash_obj)

'''


def get_hash_of_html(html_string):
    hash_object = hashlib.md5(html_string.encode('utf-8'))
    hash_of_html = hash_object.hexdigest()
    return hash_of_html


def get_data():
    data_list = []
    try:
        url = 'https://www.bis.doc.gov/dpl/public/dpl.php'
        driver.get(url)
        time.sleep(5)
        li = driver.find_elements(By.XPATH, f'/html/body/div/table/tbody/tr')

        for i in range(1, len(li), 2):
            data_dict = {}
            name = ''
            address = ''
            Effective_Date = ''
            Expiration_Date = ''
            Denial_type = ''
            summary = ''

            try:
                name, address = driver.find_element(By.XPATH, f"/html/body/div/table/tbody/tr[{i}]/td[1]").text.split("\n")
            except Exception:
                pass

            try:
                Effective_Date = driver.find_element(By.XPATH, f"/html//div/table/tbody/tr[{i}]/td[2]").text
            except Exception:
                pass

            try:
                Expiration_Date = driver.find_element(By.XPATH, f"/html//div/table/tbody/tr[{i}]/td[3]").text
            except Exception:
                pass

            try:
                Denial_type = driver.find_element(By.XPATH, f"/html//div/table/tbody/tr[{i}]/td[4]").text
            except Exception:
                pass

            try:
                summary = driver.find_element(By.XPATH, f"/html/body/div/table/tbody/tr[{i + 1}]/td").text
            except Exception:
                pass

            data_dict['fullName'] = name
            data_dict['address'] = address
            data_dict['Effective_Date'] = Effective_Date
            data_dict['Expiration_Date'] = Expiration_Date
            data_dict['Denial_type'] = Denial_type
            data_dict['summary'] = summary
            html_hash = get_hash_of_html(str(data_dict))
            data_dict['EmployeeName'] = "Ansuman Sahu"
            data_dict['UpdationFlag'] = False
            data_dict['RawHtml'] = html_hash
            data_dict['LastUpdatedDev'] = last_updated_dev
            data_dict['UpdateLabelTs'] = update_label_ts
            data_list.append(data_dict)


    except Exception:
        pass

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list1 = get_data()
    # to_json(data_list3)
    print(data_list1)
