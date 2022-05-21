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
        url = 'http://www.ntcc.crimestoppersweb.com/sitemenu.aspx?P=wanteds&ID=197'
        driver.get(url)
        time.sleep(5)
        li = driver.find_elements(By.XPATH,f'/html/body/div[1]/div[4]/div[1]/div/div[2]/div["+i+"]')

        # for i in range(2, len(li)+1):
        for i in range(2, 9):
            data_dict = {}
            name = ''
            alias = ''
            gender = ''
            race = ''
            age = ''
            height = ''
            weight = ''
            hair = ''
            eyes = ''
            Wanted_By = ''
            Wanted_For = ''
            summary = ''

            try:
                name = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[1]/div/div[2]/div[{i}]/div[2]/table/tbody/tr[2]/td[2]/span").text
            except Exception:
                pass

            try:
                summary = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[1]/div/div[2]/div[{i}]/div[2]/table/tbody/tr[1]/td/div[2]").text
            except Exception:
                pass

            try:
                alias_tag = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[1]/div/div[2]/div[{i}]/div[2]/table/tbody/tr[3]/td[1]/span").text
                if alias_tag == "Alias:":
                    alias = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[1]/div/div[2]/div[{i}]/div[2]/table/tbody/tr[3]/td[2]").text
                else:
                    alias = "None Found"
            except Exception:
                pass

            try:
                if alias_tag == "Alias:":
                    gender = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[1]/div/div[2]/div[{i}]/div[2]/table/tbody/tr[4]/td[2]").text
                else:
                    gender = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[1]/div/div[2]/div[{i}]/div[2]/table/tbody/tr[3]/td[2]").text
            except Exception:
                pass

            try:
                if alias_tag == "Alias:":
                    race = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[1]/div/div[2]/div[{i}]/div[2]/table/tbody/tr[4]/td[5]").text
                else:
                    race = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[1]/div/div[2]/div[{i}]/div[2]/table/tbody/tr[3]/td[5]").text
            except Exception:
                pass

            try:
                if alias_tag == "Alias:":
                    age = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[1]/div/div[2]/div[{i}]/div[2]/table/tbody/tr[5]/td[5]").text
                else:
                    age = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[1]/div/div[2]/div[{i}]/div[2]/table/tbody/tr[4]/td[5]").text
            except Exception:
                pass

            try:
                if alias_tag == "Alias:":
                    height = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[1]/div/div[2]/div[{i}]/div[2]/table/tbody/tr[6]/td[2]").text
                else:
                    height = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[1]/div/div[2]/div[{i}]/div[2]/table/tbody/tr[5]/td[2]").text
            except Exception:
                pass

            try:
                if alias_tag == "Alias:":
                    weight = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[1]/div/div[2]/div[{i}]/div[2]/table/tbody/tr[6]/td[5]").text
                else:
                    weight = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[1]/div/div[2]/div[{i}]/div[2]/table/tbody/tr[5]/td[5]").text
            except Exception:
                pass

            try:
                if alias_tag == "Alias:":
                    hair = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[1]/div/div[2]/div[{i}]/div[2]/table/tbody/tr[7]/td[2]").text
                else:
                    hair = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[1]/div/div[2]/div[{i}]/div[2]/table/tbody/tr[6]/td[2]").text
            except Exception:
                pass

            try:
                if alias_tag == "Alias:":
                    eyes = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[1]/div/div[2]/div[{i}]/div[2]/table/tbody/tr[7]/td[5]").text
                else:
                    eyes = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[1]/div/div[2]/div[{i}]/div[2]/table/tbody/tr[6]/td[5]").text
            except Exception:
                pass

            try:
                if alias_tag == "Alias:":
                    Wanted_By = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[1]/div/div[2]/div[{i}]/div[2]/table/tbody/tr[9]/td").text.replace("Wanted By: ", "")
                else:
                    Wanted_By = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[1]/div/div[2]/div[{i}]/div[2]/table/tbody/tr[8]/td").text.replace("Wanted By: ", "")
            except Exception:
                pass

            try:
                Wanted_For = driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[1]/div/div[2]/div[{i}]/div[2]/table/tbody/tr[1]/td/div[1]").text
            except Exception:
                pass

            data_dict['fullName'] = name
            data_dict['alias'] = alias
            data_dict['gender'] = gender
            data_dict['race'] = race
            data_dict['age'] = age
            data_dict['height'] = height
            data_dict['weight'] = weight
            data_dict['hair'] = hair
            data_dict['eyes'] = eyes
            data_dict['Wanted_By'] = Wanted_By
            data_dict['Wanted_For'] = Wanted_For
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
