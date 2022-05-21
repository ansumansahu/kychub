'''
Month_assigned : March
Date Submitted : 31-03-2022
Date_source_name : Members of the Parliament Assembly of the Republic of Kosovo
Data_source_URL : https://www-kuvendikosoves-org.translate.goog/shq/deputetet/?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp
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

options = webdriver.ChromeOptions()
prefs = {
    "translate_whitelists": {"sq": "en"},
    "translate": {"enabled": "true"}
}
options.add_experimental_option("prefs", prefs)

PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver\\chromedriver.exe"
driver = webdriver.Chrome(options=options, executable_path=PATH)
driver.maximize_window()


# def to_json(data_list):
#     hash_obj = json.dumps(data_list)
#     with open('json/dictionary.json', 'w') as ts:
#         ts.write(hash_obj)


def get_hash_of_html(html_string):
    hash_object = hashlib.md5(html_string.encode('utf-8'))
    hash_of_html = hash_object.hexdigest()
    return hash_of_html


# def get_soup(url):
#     res = requests.get(url)
#     soup = bs(res.text, 'html.parser')
#     return soup


def get_data(slug_name):
    data_list = []
    try:
        # url = 'https://www.kuvendikosoves.org/shq/deputetet/'
        url = 'https://www-kuvendikosoves-org.translate.goog/shq/deputetet/?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp'
        driver.get(url)
        time.sleep(3)

        li = driver.find_elements(By.XPATH,f'/html/body/section[2]/div/div')

        for i in range(3, len(li)+1):
            li2 = driver.find_elements(By.XPATH, f'/html/body/section[2]/div/div[{i}]/div/div')
            print(len(li2))

            for j in range(1, len(li2)+1):
                data_dict = {}
                fullName = ''
                image = ''
                politicalPartyName = ''
                website = ''
                nationality = ''
                dob = ''
                placeOfBirthCity = ''
                maritalStatus = ''
                educationInfo = ''
                languagesKnown = ''
                careerInfoRoles = ''
                additionalInfo = ''
                summary = ''

                try:
                    fullName = driver.find_element(By.XPATH, f'/html/body/section[2]/div/div[{i}]/div/div[{j}]/a/h4').text.strip()
                except Exception:
                    pass

                try:
                    image = driver.find_element(By.XPATH, f'/html/body/section[2]/div/div[{i}]/div/div[{j}]/a/img').get_attribute('src')
                except Exception:
                    pass

                try:
                    website = driver.find_element(By.XPATH, f'/html/body/section[2]/div/div[{i}]/div/div[{j}]/a/span[2]').text.strip()
                except Exception:
                    pass

                try:
                    driver.find_element(By.XPATH, f'/html/body/section[2]/div/div[{i}]/div/div[{j}]/a').click()
                    time.sleep(1)

                    driver.find_element(By.XPATH, '/html/body/section/div/div/div[1]/div/div[2]/button/span').click()
                    time.sleep(1)

                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    driver.execute_script("window.scrollTo(0, 1000);")
                    time.sleep(1)

                    try:
                        temp = driver.find_element(By.XPATH, '/html/body/section/div/div/div[1]/div/div[2]/div[1]/p[1]').text
                        politicalPartyName = temp.split(':')[1].strip()
                    except Exception:
                        pass

                    try:
                        temp = driver.find_element(By.XPATH, '/html/body/section/div/div/div[1]/div/div[2]/div[2]/p[1]').text.replace(";", "")
                        nationality = temp.split(':')[1].strip()
                    except Exception:
                        pass

                    try:
                        temp = driver.find_element(By.XPATH, '/html/body/section/div/div/div[1]/div/div[2]/div[2]/p[2]').text.replace(";", "")
                        dob = temp.split(':')[1].strip()
                    except Exception:
                        pass

                    try:
                        temp = driver.find_element(By.XPATH, '/html/body/section/div/div/div[1]/div/div[2]/div[2]/p[3]').text.replace(";", "")
                        placeOfBirthCity = temp.split(':')[1].strip()
                    except Exception:
                        pass

                    try:
                        temp = driver.find_element(By.XPATH, '/html/body/section/div/div/div[1]/div/div[2]/div[2]/p[4]').text.replace(";", "")
                        maritalStatus = temp.split(':')[1].strip()
                    except Exception:
                        pass

                    try:
                        temp = driver.find_element(By.XPATH, '/html/body/section/div/div/div[1]/div/div[2]/div[2]/p[5]').text.replace(";", "").replace("\n", "").replace("-", ";")
                        educationInfo = temp.split(':')[1].strip()
                    except Exception:
                        pass

                    try:
                        temp = driver.find_element(By.XPATH, '/html/body/section/div/div/div[1]/div/div[2]/div[2]/p[6]').text.replace(";", "")
                        languagesKnown = temp.split(':')[1].strip()
                    except Exception:
                        pass

                    try:
                        temp = driver.find_element(By.XPATH, '/html/body/section/div/div/div[1]/div/div[2]/div[2]/p[7]').text.replace(";", "").replace("\n", "").replace("-", ";")
                        careerInfoRoles = temp.split(':')[1].strip()
                    except Exception:
                        pass

                    try:
                        temp = driver.find_element(By.XPATH, '/html/body/section/div/div/div[1]/div/div[2]/div[1]/p[2]').text
                        additionalInfo = "PARLIAMENTARY GROUP: " + temp.split(':')[1].strip()
                    except Exception:
                        pass

                    try:
                        temp = driver.find_element(By.XPATH, '/html/body/section/div/div/div[1]/div/div[2]/div[1]/p[3]').text
                        additionalInfo += " ,COMMITTEES: " + temp.split(':')[1].strip()
                    except Exception:
                        pass

                    driver.back()
                    time.sleep(1)

                except Exception:
                    pass

                try:
                    summary = fullName + " is a Deputy of The Assembly of Kosovo and a member of " + politicalPartyName + " political party"
                except Exception:
                    pass

                if fullName:
                    data_dict['fullName'] = fullName
                    data_dict['image'] = image
                    data_dict['politicalPartyName'] = politicalPartyName
                    data_dict['website'] = website
                    data_dict['dob'] = dob
                    data_dict['placeOfBirthCity'] = placeOfBirthCity
                    data_dict['nationality'] = nationality
                    data_dict['maritalStatus'] = maritalStatus
                    data_dict['educationInfo'] = educationInfo
                    data_dict['languagesKnown'] = languagesKnown
                    data_dict['careerInfoRoles'] = careerInfoRoles
                    data_dict['additionalInfo'] = additionalInfo
                    data_dict['summary'] = summary
                    html_hash = get_hash_of_html(str(data_dict))
                    data_dict['EmployeeName'] = "Ansuman Sahu"
                    data_dict['UpdationFlag'] = True
                    data_dict['RawHtml'] = html_hash
                    data_dict['LastUpdatedDev'] = last_updated_dev
                    data_dict['UpdateLabelTs'] = update_label_ts
                    data_list.append(data_dict)
                    print(data_dict)

    except Exception:
        pass

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list1 = get_data('add-slug-here')
    # to_json(data_list3)
    print(data_list1)
