'''
Month_assigned : March
Date Submitted : 29-03-2022
Date_source_name :Mexico Senators directory
Data_source_URL : http://www.senado.gob.mx/64/senadores/directorio_de_senadores
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
driver = webdriver.Chrome(options=options, executable_path=PATH)
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
        url = 'https://www.senado.gob.mx/64/senadores/directorio_de_senadores'
        driver.get(url)
        time.sleep(2)

        li = driver.find_elements(By.XPATH,f"/html/body/div[3]/div/div[2]/table/tbody/tr")

        for i in range(1, len(li)+1):
            data_dict = {}
            fullName = ''
            nationality = ''
            politicalPartyName = ''
            telephoneNos = ''
            emails = ''
            additionalInfo = ''
            addressLine1 = ''
            otherSocialUrls = ''
            summary = ''

            try:
                name = driver.find_element(By.XPATH, f"/html/body/div[3]/div/div[2]/table/tbody/tr[{i}]/td[3]").text
                surname = driver.find_element(By.XPATH, f"/html/body/div[3]/div/div[2]/table/tbody/tr[{i}]/td[2]").text
                fullName = name + " " + surname
                print(fullName)
            except Exception:
                pass

            try:
                politicalPartyName = driver.find_element(By.XPATH, f"/html/body/div[3]/div/div[2]/table/tbody/tr[{i}]/td[4]").text
                print(politicalPartyName)
            except Exception:
                pass

            try:
                temp = driver.find_element(By.XPATH, f"/html/body/div[3]/div/div[2]/table/tbody/tr[{i}]/td[5]").text
                telephoneNos = "01 (55) " + " ".join(temp.split()[0:2])
                print(telephoneNos)
            except Exception:
                pass

            try:
                emails = driver.find_element(By.XPATH, f"/html/body/div[3]/div/div[2]/table/tbody/tr[{i}]/td[6]").text
                print(emails)
            except Exception:
                pass

            try:
                driver.find_element(By.XPATH,f"/html/body/div[3]/div/div[2]/table/tbody/tr[{i}]/td[2]/a").click()
                time.sleep(2)

                try:
                    temp = driver.find_element(By.XPATH,f"/html/body/div[3]/div[1]/div[2]/div/table/tbody/tr[2]/td").text
                    additionalInfo = "Alternate Name: " + temp
                    print(additionalInfo)
                except Exception:
                    pass

                try:
                    addressLine1 = driver.find_element(By.XPATH,f"/html/body/div[3]/div[1]/div[2]/div/table/tbody/tr[3]/td").text
                    print(addressLine1)
                except Exception:
                    pass

                try:
                    temp = driver.find_element(By.XPATH,f"/html/body/div[3]/div[1]/div[1]/div/div[4]/table/tbody/tr[2]/th[2]").text.replace("\n"," ")
                    politicalPartyName += "(" + temp + ")"
                    print(politicalPartyName)
                except Exception:
                    pass

                try:
                    li2 = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div[1]/div/div[3]/ul/li')
                    temp = ''
                    for ele in li2:
                        temp += ele.get_attribute('href') + ", "
                    if temp:
                        otherSocialUrls = temp.strip()[:-1]
                    print(otherSocialUrls)
                except Exception:
                    pass

                driver.back()

            except Exception:
                pass

            try:
                summary = fullName + " is a Member of Parliament of Mexico and also a member of party " + politicalPartyName
            except Exception:
                pass

            if fullName:
                data_dict['fullName'] = fullName
                data_dict['politicalPartyName'] = politicalPartyName
                data_dict['telephoneNos'] = telephoneNos
                data_dict['emails'] = emails
                data_dict['nationality'] = "Mexican"
                data_dict['addressLine1'] = addressLine1
                data_dict['additionalInfo'] = additionalInfo
                data_dict['otherSocialUrls'] = otherSocialUrls
                data_dict['summary'] = summary
                html_hash = get_hash_of_html(str(data_dict))
                data_dict['EmployeeName'] = "Ansuman Sahu"
                data_dict['UpdationFlag'] = True
                data_dict['RawHtml'] = html_hash
                data_dict['LastUpdatedDev'] = last_updated_dev
                data_dict['UpdateLabelTs'] = update_label_ts
                print(data_dict)
                data_list.append(data_dict)

    except Exception:
        pass

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    print(data_list)
