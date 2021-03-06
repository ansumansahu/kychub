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


def to_json(data_list):
    hash_obj = json.dumps(data_list)
    with open('json/dictionary.json', 'w') as ts:
        ts.write(hash_obj)


# def get_soup(url):
#     res = requests.get(url)
#     soup = bs(res.text, 'html.parser')
#     return soup


def get_hash_of_html(html_string):
    hash_object = hashlib.md5(html_string.encode('utf-8'))
    hash_of_html = hash_object.hexdigest()
    return hash_of_html


def get_data(slug_name):
    last_updated_dev = int(time.time())
    update_label_ts = int(time.time())

    options = webdriver.ChromeOptions()
    prefs = {
        "translate_whitelists": {"ru": "en"},
        "translate": {"enabled": "true"}
    }
    options.add_experimental_option("prefs", prefs)

    PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver_win32_101\\chromedriver.exe"
    driver = webdriver.Chrome(PATH, options=options)
    driver.maximize_window()

    data_list = []
    url = 'http://parliament.gov.uz/ru/structure/deputy/?abs=%D0%90'
    # url = 'https://parliament-gov-uz.translate.goog/ru/structure/deputy/?abs=%D0%90&_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp'

    driver.get(url)
    time.sleep(2)

    li = driver.find_elements(By.XPATH, f'/html/body/div[1]/div/div[2]/div[1]/div[2]/div/ul/li/a')
    for k in range(1, len(li)+1):
        try:
            driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[2]/div[1]/div[2]/div/ul/li[{k}]/a').click()
            time.sleep(3)

            li2 = driver.find_elements(By.XPATH,f"/html/body/div[1]/div/div[2]/div[1]/div[3]/div/div/div/div[2]/h5/a")
            # print(len(li2))
            for i in range(1, len(li2)+1):
                driver.find_element(By.XPATH,f"/html/body/div[1]/div/div[2]/div[1]/div[3]/div/div[{i}]/div/div[2]/h5/a").click()
                time.sleep(3)

                try:
                    data_section = driver.find_elements(By.CSS_SELECTOR,'div.col-md-9.col-md-push-3.col-xs-12.center_main_content_block')
                    for data_sec in data_section:
                        if data_sec:
                            data_dict = {}
                            fullName = ''
                            designation = ''
                            image = ''
                            dob = ''
                            placeOfBirthCity = ''
                            nationality = ''
                            educationInfo = ''
                            languagesKnown = ''
                            region = ''
                            constituency = ''
                            listOfCommitteeInfo = ''
                            politicalPartyName = ''
                            summary = ''
                            additionalInfo = ''

                            try:
                                fullName = data_sec.find_element(By.CSS_SELECTOR, 'h3').text.strip()
                            except Exception:
                                pass

                            try:
                                designation = data_sec.find_element(By.CSS_SELECTOR, 'div.col-md-9.col-sm-9.col-xs-12.deputats_info > p:nth-child(1) > span').text.replace(
                                    '-', '').strip()
                            except Exception:
                                pass

                            try:
                                dob = data_sec.find_element(By.CSS_SELECTOR, 'div.col-md-9.col-sm-9.col-xs-12.deputats_info > p:nth-child(2) > span').text.strip()
                            except Exception:
                                pass

                            try:
                                placeOfBirthCity = data_sec.find_element(By.CSS_SELECTOR, 'div.col-md-9.col-sm-9.col-xs-12.deputats_info > p:nth-child(3) > span').text.replace('-', '').strip()
                            except Exception:
                                pass

                            try:
                                nationality = data_sec.find_element(By.CSS_SELECTOR, 'div.col-md-9.col-sm-9.col-xs-12.deputats_info > p:nth-child(4) > span').text.replace('-', '').strip()
                            except Exception:
                                pass

                            try:
                                educationInfo = data_sec.find_element(By.CSS_SELECTOR, 'div.col-md-9.col-sm-9.col-xs-12.deputats_info > p:nth-child(5) > span').text.replace('-', '').strip()
                            except Exception:
                                pass

                            try:
                                temp = data_sec.find_element(By.CSS_SELECTOR, 'div.col-md-9.col-sm-9.col-xs-12.deputats_info > p:nth-child(6) > span').text.replace('-', '').strip()
                                if temp:
                                    educationInfo += " ,Place of Study : " + temp
                            except Exception:
                                pass

                            try:
                                temp = data_sec.find_element(By.CSS_SELECTOR, 'div.col-md-9.col-sm-9.col-xs-12.deputats_info > p:nth-child(7) > span').text.replace('-', '').strip()
                                additionalInfo = "Speciality: " + temp
                            except Exception:
                                pass

                            try:
                                languagesKnown = data_sec.find_element(By.CSS_SELECTOR, 'div.col-md-9.col-sm-9.col-xs-12.deputats_info > p:nth-child(10) > span').text.replace('-', '').strip()
                            except Exception:
                                pass

                            try:
                                region = data_sec.find_element(By.CSS_SELECTOR, 'div.list-group.deputats_info > div > p:nth-child(1) > span').text.replace('-', '').strip()
                            except Exception:
                                pass

                            try:
                                constituency = data_sec.find_element(By.CSS_SELECTOR, 'div.list-group.deputats_info > div > p:nth-child(2) > span').text.replace('-', '').strip()
                            except Exception:
                                pass

                            try:
                                listOfCommitteeInfo = data_sec.find_element(By.CSS_SELECTOR, 'div.list-group.deputats_info > div > p:nth-child(3) > span').text.replace('-', '').strip()
                            except Exception:
                                pass

                            try:
                                temp = data_sec.find_element(By.CSS_SELECTOR, 'div.list-group.deputats_info > div > p:nth-child(4) > span').text.replace('-', '').strip()
                                if temp:
                                    additionalInfo += " ,Faction member: " + temp
                            except Exception:
                                pass

                            try:
                                politicalPartyName = data_sec.find_element(By.CSS_SELECTOR, 'div.list-group.deputats_info > div > p:nth-child(6) > span').text.replace('-', '').strip()
                            except Exception:
                                pass

                            try:
                                temp = data_sec.find_element(By.CSS_SELECTOR, 'div.list-group.deputats_info > div > p:nth-child(7) > span').text.replace('-', '').strip()
                                if temp:
                                    additionalInfo += " ,Participation in elected bodies of power: " + temp
                            except Exception:
                                pass

                            try:
                                temp = data_sec.find_element(By.CSS_SELECTOR, 'div.list-group.deputats_info > div > p:nth-child(8) > span').text.replace('-', '').strip()
                                if temp:
                                    additionalInfo += " ,State awards: " + temp
                            except Exception:
                                pass

                            try:
                                if fullName and politicalPartyName:
                                    summary = fullName + " is a Member of Parliament of Uzbekistan and a member of " + politicalPartyName
                                else:
                                    summary = fullName + " is a Member of Parliament of Uzbekistan"
                            except Exception:
                                pass

                            try:
                                image = data_sec.find_element(By.CSS_SELECTOR, 'div.col-md-3.col-sm-3.col-xs-12 > img').get_attribute('src')
                            except Exception:
                                pass

                            if fullName:
                                data_dict['fullName'] = fullName
                                data_dict['image'] = image
                                data_dict['designation'] = designation
                                data_dict['dob'] = dob
                                data_dict['placeOfBirthCity'] = placeOfBirthCity
                                data_dict['nationality'] = nationality
                                data_dict['educationInfo'] = educationInfo
                                data_dict['languagesKnown'] = languagesKnown
                                data_dict['region'] = region
                                data_dict['constituency'] = constituency
                                data_dict['listOfCommitteeInfo'] = listOfCommitteeInfo
                                data_dict['politicalPartyName'] = politicalPartyName
                                data_dict['additionalInfo'] = additionalInfo
                                data_dict['summary'] = summary
                                # print(data_dict)
                                data_dict['UpdationFlag'] = True
                                html_hash = get_hash_of_html(str(data_dict))
                                data_dict['RawHtml'] = html_hash
                                data_dict['LastUpdatedDev'] = last_updated_dev
                                data_dict['UpdateLabelTs'] = update_label_ts

                            if data_dict:
                                data_list.append(data_dict)

                except Exception:
                    pass

                driver.back()
                time.sleep(3)

        except Exception as e:
            print(e)
            pass

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    # print(data_list)
