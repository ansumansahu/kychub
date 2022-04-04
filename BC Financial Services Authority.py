'''
Month_assigned : March
Date Submitted : 31-03-2022
Date_source_name : BC Financial Services Authority (BCFSA)
Harvesting_URL : https://www.bcfsa.ca/index.aspx?p=about_us/boardMembers
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


# def get_soup(url):
#     res = requests.get(url)
#     soup = bs(res.text, 'html.parser')
#     return soup


def get_data(slug_name):
    data_list = []
    try:
        url = 'https://www.bcfsa.ca/index.aspx?p=about_us/boardMembers'
        driver.get(url)
        time.sleep(1)

        li = driver.find_elements(By.CSS_SELECTOR, f'button.g-accordion-item__label')
        for i in range(len(li)):
            try:
                print(i)
                li[i].click()
                time.sleep(3)

                data_dict = {}
                fullName = ''
                image = ''
                designation = ''
                category = ''
                summary = ''
                careerInfoStartDate = ''
                careerInfoEndDate = ''

                try:
                    temp = driver.find_element(By.XPATH, f'/html/body/div/div/main/div/article/div[2]/div/ul/li[{i+1}]/button/h3').text
                    temp2 = temp.replace('\u202f—\u2009', '-')
                    if '-' in temp2:
                        fullName = temp2.split('-')[0].strip()
                        designation = temp2.split('-')[1].strip()
                    else:
                        fullName = temp.strip()
                        designation = "Director"
                except Exception:
                    pass

                try:
                    image = driver.find_element(By.XPATH, f'/html/body/div/div/main/div/article/div[2]/div/ul/li[{i+1}]/div/figure/picture/img').get_attribute('src')
                except Exception:
                    pass

                try:
                    temp = driver.find_element(By.XPATH, f'/html/body/div/div/main/div/article/div[2]/div/ul/li[{i+1}]/div/p[2]').text
                    print(temp)
                    temp2 = temp.split(':')[1]
                    careerInfoStartDate = temp2.split('–')[0].strip()
                    careerInfoEndDate = temp2.split('–')[1].strip()
                except Exception:
                    pass

                summary = "BC Financial Services Authority is overseen by " + fullName + "as a member of Board of Directors appointed by the Lieutenant Governor in Council"

                if fullName:
                    data_dict['fullName'] = fullName
                    data_dict['designation'] = designation
                    data_dict['image'] = image
                    data_dict['category'] = 'Individual'
                    data_dict['careerInfoStartDate'] = careerInfoStartDate
                    data_dict['careerInfoEndDate'] = careerInfoEndDate
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

    except Exception:
        pass

    driver.quit()

    return data_list


if __name__ == "__main__":
    data_list1 = get_data('add-slug-here')
    # to_json(data_list3)
    print(data_list1)