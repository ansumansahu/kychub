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
import json

PATH = "C:\\Users\\91702\\Downloads\\chromedriver_win32\\chromedriver.exe"
# PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver\\chromedriver.exe"
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(PATH)
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
        url = 'https://www.president.ir/en/president/cabinet#'
        driver.get(url)
        time.sleep(5)
        try:
            ministers_title = driver.find_elements(By.XPATH,f"//div[@id='cabinet']/div/div[@class='row']/div/div/p[@class='title']")
            ministers_title_text=[]
            for i in ministers_title:
                ministers_title_text.append(i.text)
        except Exception:
            pass

        try:
            ministers_names = driver.find_elements(By.XPATH,f"//div[@id='cabinet']/div/div[@class='row']/div/div/p[@class='name']")
            ministers_names_text = []
            for i in ministers_names:
                ministers_names_text.append(i.text)
        except Exception:
            pass

        try:
            images = driver.find_elements(By.XPATH,f"//div[@id='cabinet']/div//img")
            images_text = []
            for i in range(len(images)):
                images_text.append(images[i].get_attribute('src'))
        except Exception:
            pass

        try:
            x = driver.find_element(By.XPATH,f"//div[@id='cabinet']//div[@class='title']")
            x = x.text
            y = x.split("\n")
            data_dict={}
            data_dict["fullName"] = y[0]
            data_dict["designation"] = y[1]
            data_dict["image"] = images_text[0]
            html_hash = get_hash_of_html(str(data_dict))
            data_dict['EmployeeName'] = "Romit Singh"
            data_dict['UpdationFlag'] = False
            data_dict['RawHtml'] = html_hash
            data_dict['LastUpdatedDev'] = last_updated_dev
            data_dict['UpdateLabelTs'] = update_label_ts
            data_list.append(data_dict)

        except Exception:
            pass

        for i in range(len(images_text)):
            data_dict = {}
            data_dict["fullName"] = ministers_names_text[i]
            data_dict["designation"] = ministers_title_text[i]
            data_dict["image"] = images_text[i+1]
            html_hash = get_hash_of_html(str(data_dict))
            data_dict['EmployeeName'] = "Romit Singh"
            data_dict['UpdationFlag'] = False
            data_dict['RawHtml'] = html_hash
            data_dict['LastUpdatedDev'] = last_updated_dev
            data_dict['UpdateLabelTs'] = update_label_ts
            data_list.append(data_dict)

        driver.quit()
    except (Exception):
        pass
    return data_list

if __name__ == "__main__":
    data_list3 = get_data()
    # to_json(data_list3)
    print(data_list3)