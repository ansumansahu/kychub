'''
Month_assigned : May
Date Submitted : 06-05-2022
Date_source_name : mansfield jail inmates
Data_source_URL : https://p2c.mansfieldtexas.gov/jailinmates.aspx
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


def get_soup(url):
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')
    return soup


def get_data(slug_name):
    last_updated_dev = int(time.time())
    update_label_ts = int(time.time())

    PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver\\chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(PATH)
    driver.maximize_window()

    data_list = []
    url = 'https://p2c.mansfieldtexas.gov/jailinmates.aspx'
    driver.get(url)
    time.sleep(1)

    try:
        driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]/div[2]/div/div[5]/div/table/tbody/tr/td[2]/table/tbody/tr/td[5]/select').click()
        time.sleep(2)
    except Exception as e:
        print(e)

    try:
        driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]/div[2]/div/div[5]/div/table/tbody/tr/td[2]/table/tbody/tr/td[5]/select/option[5]').click()
        time.sleep(2)
    except Exception as e:
        print(e)

    try:
        li = driver.find_elements(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]/div[2]/div/div[3]/div[3]/div/table/tbody/tr')
        for i in range(1, len(li)+1):
            data_dict = {}
            fullName = ''
            image = ''
            age = ''
            charges = ''
            gender = ''
            race = ''
            importantDates = ''
            additionalInfo = ''

            try:
                driver.find_element(By.XPATH, f'/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]/div[2]/div/div[3]/div[3]/div/table/tbody/tr[{i}]').click()
                time.sleep(1)

                try:
                    temp = driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]/div[1]/div/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/p/span').text.strip()
                    fullName = temp.split(",")[1].strip() + " " + temp.split(",")[0].strip()
                except Exception:
                    pass

                try:
                    image = driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]/div[1]/div/table/tbody/tr/td[2]/img').get_attribute('src')
                except Exception:
                    pass

                try:
                    age = driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]/div[1]/div/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/p/span').text.strip()
                except Exception:
                    pass

                try:
                    race = driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]/div[1]/div/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/span[1]').text.strip()
                except Exception:
                    pass

                try:
                    gender = driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]/div[1]/div/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/span[3]').text.strip()
                except Exception:
                    pass

                try:
                    importantDates = "Arrest Date: " + driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]/div[1]/div/table/tbody/tr/td[1]/table/tbody/tr[4]/td[2]/span').text.strip()
                except Exception:
                    pass

                try:
                    importantDates += ", Release Date: " + driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]/div[1]/div/table/tbody/tr/td[1]/table/tbody/tr[5]/td[2]/span').text.strip()
                except Exception:
                    pass

                try:
                    importantDates += ", Next Court Date: " + driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]/div[1]/div/table/tbody/tr/td[1]/table/tbody/tr[6]/td[2]/span').text.strip()
                except Exception:
                    pass

                try:
                    li2 = driver.find_elements(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]/div[2]/div/div/table/tbody/tr')
                    for j in range(2, len(li2)+1):
                        charges += driver.find_element(By.XPATH, f'/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]/div[2]/div/div/table/tbody/tr[{j}]/td[1]').text.strip() + ", "
                except Exception:
                    pass

                try:
                    additionalInfo = "Total Bond Amount: " + driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]/div[2]/table/tbody/tr/td/span[2]').text.strip()
                except Exception:
                    pass

                if fullName:
                    data_dict['fullName'] = fullName
                    data_dict['image'] = image
                    data_dict['category'] = 'CRIME'
                    data_dict['age'] = age
                    data_dict['gender'] = gender
                    data_dict['race'] = race
                    data_dict['importantDates'] = importantDates
                    data_dict['charges'] = charges.strip().removesuffix(",")
                    data_dict['additionalInfo'] = additionalInfo
                    data_dict['summary'] = fullName + " is an Inmate listed by Mansfield Police Department"
                    # print(data_dict)
                    data_dict['UpdationFlag'] = True
                    html_hash = get_hash_of_html(str(data_dict))
                    data_dict['RawHtml'] = html_hash
                    data_dict['LastUpdatedDev'] = last_updated_dev
                    data_dict['UpdateLabelTs'] = update_label_ts

                if data_dict:
                    data_list.append(data_dict)

                driver.back()
                time.sleep(1)

            except Exception:
                pass

    except Exception:
        pass

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    # print(data_list)
