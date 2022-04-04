'''
Month_assigned : March
Date Submitted : 31-03-2022
Date_source_name : Deputies Of Legislative Assembly Republic of Costa Rica
Harvesting_URL : http://www.asamblea.go.cr/Diputados/SitePages/Inicio.aspx
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
        # url = 'http://www.asamblea.go.cr/Diputados/SitePages/Inicio.aspx'
        url = 'https://www-asamblea-go-cr.translate.goog/Diputados/SitePages/Inicio.aspx?_x_tr_sch=http&_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp'
        driver.get(url)
        time.sleep(1)

        li = driver.find_elements(By.XPATH,f'/html/body/form/div[4]/div[3]/div/div/div[4]/div/div/div/div/div[2]/div/div[4]/div/div/table/tbody/tr/td/div/div/table[2]/tbody/tr')

        for i in range(15, len(li)+1):
            li2 = driver.find_elements(By.XPATH,f'/html/body/form/div[4]/div[3]/div/div/div[4]/div/div/div/div/div[2]/div/div[4]/div/div/table/tbody/tr/td/div/div/table[2]/tbody/tr[{i}]/td')

            for j in range(2, len(li2)+1, 2):
                driver.find_element(By.XPATH,f'/html/body/form/div[4]/div[3]/div/div/div[4]/div/div/div/div/div[2]/div/div[4]/div/div/table/tbody/tr/td/div/div/table[2]/tbody/tr[{i}]/td[{j}]/div/li/ul/h5').click()
                time.sleep(1)

                data_dict = {}
                fullName = ''
                image = ''
                emails = ''
                politicalPartyName = ''
                stateProvince = ''
                country = ''
                dob = ''
                placeOfBirthCity = ''
                facebookUrl = ''
                twitterUrl = ''
                maritalStatus = ''
                careerInfo = ''
                careerInfoStartDate = ''
                summary = ''

                try:
                    fullName = driver.find_element(By.XPATH, '/html/body/form/div[4]/div[3]/div/div/div[3]/table/tbody/tr[1]/td/h1').text.strip()
                except Exception:
                    pass

                try:
                    image = driver.find_element(By.XPATH, '/html/body/form/div[4]/div[3]/div/div/table[2]/tbody/tr/td[1]/blockquote/img').get_attribute('src').replace("https://translate.google.com/website?sl=auto&tl=en&hl=en&client=webapp&u=", "")
                except Exception:
                    pass

                try:
                    data_section = driver.find_elements(By.XPATH, f'/html/body/form/div[4]/div[3]/div/div/table[2]/tbody/tr/td[2]/blockquote')
                    k = len(data_section)
                    for data_sec in data_section:
                        temp = data_sec.text
                        if "Place and date of birth:" in temp:
                            temp = temp.split('/')[0].split(':')[1]
                            dob = ",".join(temp.split(',')[-2:]).strip()
                            placeOfBirthCity = ",".join(temp.split(',')[:-2]).strip()
                        if "Profession:" in temp:
                            careerInfo = temp.split(':')[1].strip()
                        if "Marital Status" in temp:
                            maritalStatus = temp.split(':')[1].strip()
                        if "Province:" in temp:
                            stateProvince = temp.split(':')[1].strip()
                        if "Period:" in temp:
                            careerInfoStartDate = temp.split(':')[1].split('-')[0].strip()
                        if "Parliamentary Faction" in temp:
                            politicalPartyName = temp.split(':')[1].strip()
                        if "Email" in temp:
                            print(temp)
                            emails = temp.replace('Email', '').replace('&ZeroWidthSpace;', '').replace(":", "").strip()

                        try:
                            li3 = driver.find_elements(By.XPATH,f'/html/body/form/div[4]/div[3]/div/div/table[2]/tbody/tr/td[2]/blockquote[{k}]/a')
                            for ele in li3:
                                temp = ele.get_attribute('href')
                                if "facebook" in temp:
                                    facebookUrl = temp.replace("https://translate.google.com/website?sl=auto&tl=en&hl=en&client=webapp&u=", "").strip()
                                if "twitter" in temp:
                                    twitterUrl = temp.replace("https://translate.google.com/website?sl=auto&tl=en&hl=en&client=webapp&u=", "").strip()

                        except Exception:
                            pass

                except Exception:
                    pass

                try:
                    summary = fullName + " is a members of the Legislative Assembly of Costa Rica"
                except Exception:
                    pass

                if fullName:
                    data_dict['fullName'] = fullName
                    data_dict['image'] = image
                    data_dict['emails'] = emails
                    data_dict['politicalPartyName'] = politicalPartyName
                    data_dict['stateProvince'] = stateProvince
                    data_dict['dob'] = dob
                    data_dict['placeOfBirthCity'] = placeOfBirthCity
                    data_dict['country'] = "Costa Rica"
                    data_dict['facebookUrl'] = facebookUrl
                    data_dict['twitterUrl'] = twitterUrl
                    data_dict['maritalStatus'] = maritalStatus
                    data_dict['careerInfo'] = careerInfo
                    data_dict['careerInfoStartDate'] = careerInfoStartDate
                    data_dict['summary'] = summary
                    html_hash = get_hash_of_html(str(data_dict))
                    data_dict['EmployeeName'] = "Ansuman Sahu"
                    data_dict['UpdationFlag'] = True
                    data_dict['RawHtml'] = html_hash
                    data_dict['LastUpdatedDev'] = last_updated_dev
                    data_dict['UpdateLabelTs'] = update_label_ts
                    data_list.append(data_dict)
                    print(data_dict)

                driver.back()

    except Exception:
        pass

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list1 = get_data('add-slug-here')
    # to_json(data_list3)
    print(data_list1)