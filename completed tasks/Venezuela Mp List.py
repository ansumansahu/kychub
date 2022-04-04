'''
Month_assigned : March
Date Submitted : 30-03-2022
Date_source_name : Venezuela Mp List
Data_source_URL : http://www.asambleanacional.gob.ve/diputados
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
from bs4 import BeautifulSoup as soup
import time

last_updated_dev = int(time.time())
update_label_ts = int(time.time())

options = webdriver.ChromeOptions()
prefs = {
    "translate_whitelists": {"es": "en"},
    "translate": {"enabled": "true"}
}
options.add_experimental_option("prefs", prefs)

PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver\\chromedriver.exe"
# driver = webdriver.Chrome(options=options, executable_path=PATH)
# options = webdriver.ChromeOptions()
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


def get_data(slug_name):
    data_list = []
    try:
        url = 'http://www.asambleanacional.gob.ve/diputados'
        driver.get(url)
        time.sleep(1)

        while True:
            try:
                data_sec = driver.find_elements(By.CSS_SELECTOR,'div.uk-panel.uk-text-center')
                print(len(data_sec))
                for data in data_sec:
                    data_dict = {}
                    fullName = ''
                    politicalPartyName = ''
                    state = ''
                    summary = ''

                    try:
                        fullName = data.find_element(By.CSS_SELECTOR,'div.text-diputado-slider.uk-margin-top.uk-position-botton.uk-text-center > b').text
                        print(fullName)
                    except Exception:
                        pass

                    try:
                        temp = data.find_element(By.CSS_SELECTOR,'div.text-diputado-slider.uk-margin-top.uk-position-botton.uk-text-center > small:nth-child(2)').text
                        politicalPartyName = temp.replace('"', '').split(':')[1].strip()
                        print(politicalPartyName)
                    except Exception:
                        pass

                    try:
                        temp = data.find_element(By.CSS_SELECTOR,'div.text-diputado-slider.uk-margin-top.uk-position-botton.uk-text-center > small:nth-child(3)').text
                        state = temp.replace('"', '').split(':')[1].strip()
                        print(state)
                    except Exception:
                        pass

                    try:
                        summary = fullName + " is a Member of Parliament of Venezuela and also a member of " + politicalPartyName + " political party."
                    except Exception:
                        pass

                    if fullName:
                        data_dict['fullName'] = fullName
                        data_dict['politicalPartyName'] = politicalPartyName
                        data_dict['state'] = state
                        data_dict['country'] = "Venezuela"
                        data_dict['summary'] = summary
                        print(data_dict)
                        html_hash = get_hash_of_html(str(data_dict))
                        data_dict['EmployeeName'] = "Ansuman Sahu"
                        data_dict['UpdationFlag'] = True
                        data_dict['RawHtml'] = html_hash
                        data_dict['LastUpdatedDev'] = last_updated_dev
                        data_dict['UpdateLabelTs'] = update_label_ts
                        data_list.append(data_dict)

            except Exception:
                pass

            driver.find_element(By.CSS_SELECTOR, "li > a > span.uk-pagination-next").click()
            time.sleep(2)

    except Exception:
        pass

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    print(data_list)
