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

PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver\\chromedriver.exe"
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(PATH)
driver.maximize_window()


# def to_json(data_list):
#     hash_obj = json.dumps(data_list)
#     with open('json/dictionary.json', 'w') as ts:
#         ts.write(hash_obj)


def get_soup(url):
    res = requests.get(url)
    soup = bs(res.text, 'html.parser')
    return soup


def get_hash_of_html(html_string):
    hash_object = hashlib.md5(html_string.encode('utf-8'))
    hash_of_html = hash_object.hexdigest()
    return hash_of_html


def get_data(slug_name):
    url = 'https://www.fbi.gov/wanted'

    data_list = []

    driver.get(url)
    time.sleep(1)

    li = driver.find_elements(By.XPATH,
                              f"/html/body/div[1]/div[2]/div[2]/section/div/div[1]/div[1]/div[1]/div/div/div/div/div/div/div/a[1]")

    for i in range(1, len(li)+1):
    # for i in range(6, 7):
        try:
            link = driver.find_element(By.XPATH,
                                       f"/html/body/div[1]/div[2]/div[2]/section/div/div[1]/div[1]/div[1]/div/div/div/div/div/div[{i}]/div/a[1]").get_attribute(
                "href")
            print(link)
            driver.get(link)
            time.sleep(1)

            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(5)

            li2 = []
            try:
                li2 = driver.find_elements(By.XPATH,
                                           f"/html/body/div[1]/div[2]/div[2]/section/div/div[2]/div/div[2]/div/div/div[1]/div[2]/ul/li/h3/a")
                print(len(li2))

                j = 1
                while j != len(li2) + 1:
                    # print(j)

                    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    time.sleep(3)

                    try:
                        driver.find_element(By.XPATH,
                                            f"/html/body/div[1]/div[2]/div[2]/section/div/div[2]/div/div[2]/div/div/div[1]/div[2]/ul/li[{j}]/h3/a").click()
                        time.sleep(1)

                        try:
                            data_section = driver.find_elements(By.XPATH,
                                                                f'/html/body/div[1]/div[2]/div[2]/section/article/section[2]/div/div')
                            if data_section:
                                data_dict = {}
                                fullName = ''
                                summary = ''
                                additionalInfo = ''

                                try:
                                    fullName = driver.find_element(By.XPATH,
                                                                   f'/html/body/div[1]/div[2]/div[2]/section/article/section[2]/div/div/h1').text
                                    # print(fullName)
                                    data_dict['fullName'] = fullName
                                except Exception:
                                    pass

                                try:
                                    alias = driver.find_element(By.CSS_SELECTOR, 'div.wanted-person-aliases > p').text
                                    # print(alias)
                                    data_dict['alias'] = alias
                                except Exception:
                                    pass

                                try:
                                    image = driver.find_element(By.XPATH,
                                                                '/html/body/div[1]/div[2]/div[2]/section/article/section[2]/div/div/div[2]/div[1]/img').get_attribute(
                                        'src')
                                    # print(image)
                                    data_dict['image'] = image
                                except Exception:
                                    pass

                                try:
                                    temp = driver.find_element(By.XPATH,
                                                               '/html/body/div[1]/div[2]/div[2]/section/article/section[2]/div/div/div[2]/div[2]/p[1]/a').get_attribute(
                                        'href')
                                    # print(temp)
                                    additionalInfo = "Wanted Fugitive Poster : " + temp
                                except Exception:
                                    pass

                                try:
                                    li3 = driver.find_elements(By.CSS_SELECTOR, 'li.castle-grid-block-item')
                                    # print(len(li3))
                                    temp = ''
                                    for ele in range(1, len(li3) + 1):
                                        temp += driver.find_element(By.XPATH,
                                                                    f'/html/body/div[1]/div[2]/div[2]/section/article/section[2]/div/div/div[3]/div/ul/li[{ele}]/div/a').get_attribute(
                                            'href') + ", "
                                    # print(temp)
                                    if temp:
                                        additionalInfo += " More Images: " + temp
                                except Exception:
                                    pass

                                try:
                                    link = driver.find_element(By.XPATH,f'/html/head/link[1]').get_attribute('href')
                                    # print(link)
                                    soup = get_soup(link)

                                    temp = soup.find('table', {'class': 'table table-striped wanted-person-description'})
                                    temp1 = temp.find_all('tr')
                                    for data in temp1:
                                        data1 = data.text
                                        try:
                                            aliasDOb = data1.split('Date(s) of Birth Used')
                                            # print("aliasDOb : " + aliasDOb[1])
                                            data_dict['aliasDOb'] = aliasDOb[1].strip()
                                        except Exception:
                                            pass

                                        try:
                                            aliasPlaceOfBirth = data1.split('Place of Birth')
                                            # print("aliasPlaceOfBirth : " + aliasPlaceOfBirth[1])
                                            data_dict['aliasPlaceOfBirth'] = aliasPlaceOfBirth[1].strip()
                                        except Exception:
                                            pass

                                        try:
                                            hair = data1.split('Hair')
                                            # print("hair : " + hair[1])
                                            data_dict['hair'] = hair[1].strip()
                                        except Exception:
                                            pass

                                        try:
                                            eyes = data1.split('Eyes')
                                            # print("eyes : " + eyes[1])
                                            data_dict['eyes'] = eyes[1].strip()
                                        except Exception:
                                            pass

                                        try:
                                            height = data1.split('Height')
                                            # print("height : " + height[1])
                                            data_dict['height'] = height[1].strip()
                                        except Exception:
                                            pass

                                        try:
                                            weight = data1.split('Weight')
                                            # print("weight : " + weight[1])
                                            data_dict['weight'] = weight[1].strip()
                                        except Exception:
                                            pass

                                        try:
                                            gender = data1.split('Sex')
                                            # print("gender : " + gender[1])
                                            data_dict['gender'] = gender[1].strip()
                                        except Exception:
                                            pass

                                        try:
                                            race = data1.split('Race')
                                            # print("race : " + race[1])
                                            data_dict['race'] = race[1].strip()
                                        except Exception:
                                            pass

                                        try:
                                            nationality = data1.split('Nationality')
                                            # print("nationality : " + nationality[1])
                                            data_dict['nationality'] = nationality[1].strip()
                                        except Exception:
                                            pass

                                        try:
                                            distinguishMarks = data1.split('Scars and Marks')
                                            # print("distinguishMarks : " + distinguishMarks[1])
                                            data_dict['distinguishMarks'] = distinguishMarks[1].strip()
                                        except Exception:
                                            pass

                                        try:
                                            languagesKnown = data1.split('Languages')
                                            # print("languagesKnown : " + languagesKnown[1])
                                            data_dict['languagesKnown'] = languagesKnown[1].strip()
                                        except Exception:
                                            pass

                                        try:
                                            complexion = data1.split('Complexion')
                                            # print("complexion : " + complexion[1])
                                            data_dict['complexion'] = complexion[1].strip()
                                        except Exception:
                                            pass

                                        try:
                                            buildCharacteristic = data1.split('Build')
                                            # print("buildCharacteristic : " + buildCharacteristic[1])
                                            data_dict['buildCharacteristic'] = buildCharacteristic[1].strip()
                                        except Exception:
                                            pass

                                except Exception:
                                    pass

                                try:
                                    summary = fullName + " is a wanted fugitive listed by FBI"
                                except Exception:
                                    pass

                                data_dict['additionalInfo'] = additionalInfo
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

                        driver.back()

                    except Exception:
                        pass

                    j += 1

            except Exception:
                pass

            if not li2:
                try:
                    li2 = driver.find_elements(By.CSS_SELECTOR, 'li:nth-child(n) > h3 > a')
                    print(len(li2))

                    j = 1
                    while j != len(li2) + 1:
                        # print(j)

                        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                        time.sleep(3)

                        try:
                            driver.find_element(By.CSS_SELECTOR, f'li:nth-child({j}) > h3 > a').click()
                            time.sleep(1)

                            try:
                                data_section = driver.find_elements(By.XPATH,
                                                                    f'/html/body/div[1]/div[2]/div[2]/section/article/section[2]/div/div')
                                if data_section:
                                    data_dict = {}
                                    fullName = ''
                                    summary = ''
                                    additionalInfo = ''

                                    try:
                                        fullName = driver.find_element(By.XPATH,
                                                                       f'/html/body/div[1]/div[2]/div[2]/section/article/section[2]/div/div/h1').text
                                        # print(fullName)
                                        data_dict['fullName'] = fullName
                                    except Exception:
                                        pass

                                    try:
                                        alias = driver.find_element(By.CSS_SELECTOR,'div.wanted-person-aliases > p').text
                                        # print(alias)
                                        data_dict['alias'] = alias
                                    except Exception:
                                        pass

                                    try:
                                        image = driver.find_element(By.XPATH,
                                                                    '/html/body/div[1]/div[2]/div[2]/section/article/section[2]/div/div/div[2]/div[1]/img').get_attribute(
                                            'src')
                                        data_dict['image'] = image
                                    except Exception:
                                        pass

                                    try:
                                        temp = driver.find_element(By.XPATH,
                                                                   '/html/body/div[1]/div[2]/div[2]/section/article/section[2]/div/div/div[2]/div[2]/p[1]/a').get_attribute(
                                            'href')
                                        # print(temp)
                                        additionalInfo = "Wanted Fugitive Poster : " + temp
                                    except Exception:
                                        pass

                                    try:
                                        li3 = driver.find_elements(By.CSS_SELECTOR, 'li.castle-grid-block-item')
                                        # print(len(li3))
                                        temp = ''
                                        for ele in range(1, len(li3) + 1):
                                            temp += driver.find_element(By.XPATH,
                                                                        f'/html/body/div[1]/div[2]/div[2]/section/article/section[2]/div/div/div[3]/div/ul/li[{ele}]/div/a').get_attribute(
                                                'href') + ", "
                                        # print(temp)
                                        if temp:
                                            additionalInfo += " More Images: " + temp
                                    except Exception:
                                        pass

                                    try:
                                        link = driver.find_element(By.XPATH, f'/html/head/link[1]').get_attribute(
                                            'href')
                                        # print(link)
                                        soup = get_soup(link)

                                        temp = soup.find('table',
                                                         {'class': 'table table-striped wanted-person-description'})
                                        temp1 = temp.find_all('tr')
                                        for data in temp1:
                                            data1 = data.text
                                            try:
                                                aliasDOb = data1.split('Date(s) of Birth Used')
                                                # print("aliasDOb : " + aliasDOb[1])
                                                data_dict['aliasDOb'] = aliasDOb[1].strip()
                                            except Exception:
                                                pass

                                            try:
                                                aliasPlaceOfBirth = data1.split('Place of Birth')
                                                # print("aliasPlaceOfBirth : " + aliasPlaceOfBirth[1])
                                                data_dict['aliasPlaceOfBirth'] = aliasPlaceOfBirth[1].strip()
                                            except Exception:
                                                pass

                                            try:
                                                hair = data1.split('Hair')
                                                # print("hair : " + hair[1])
                                                data_dict['hair'] = hair[1].strip()
                                            except Exception:
                                                pass

                                            try:
                                                eyes = data1.split('Eyes')
                                                # print("eyes : " + eyes[1])
                                                data_dict['eyes'] = eyes[1].strip()
                                            except Exception:
                                                pass

                                            try:
                                                height = data1.split('Height')
                                                # print("height : " + height[1])
                                                data_dict['height'] = height[1].strip()
                                            except Exception:
                                                pass

                                            try:
                                                weight = data1.split('Weight')
                                                # print("weight : " + weight[1])
                                                data_dict['weight'] = weight[1].strip()
                                            except Exception:
                                                pass

                                            try:
                                                gender = data1.split('Sex')
                                                # print("gender : " + gender[1])
                                                data_dict['gender'] = gender[1].strip()
                                            except Exception:
                                                pass

                                            try:
                                                race = data1.split('Race')
                                                # print("race : " + race[1])
                                                data_dict['race'] = race[1].strip()
                                            except Exception:
                                                pass

                                            try:
                                                nationality = data1.split('Nationality')
                                                # print("nationality : " + nationality[1])
                                                data_dict['nationality'] = nationality[1].strip()
                                            except Exception:
                                                pass

                                            try:
                                                distinguishMarks = data1.split('Scars and Marks')
                                                # print("distinguishMarks : " + distinguishMarks[1])
                                                data_dict['distinguishMarks'] = distinguishMarks[1].strip()
                                            except Exception:
                                                pass

                                            try:
                                                languagesKnown = data1.split('Languages')
                                                # print("languagesKnown : " + languagesKnown[1])
                                                data_dict['languagesKnown'] = languagesKnown[1].strip()
                                            except Exception:
                                                pass

                                            try:
                                                complexion = data1.split('Complexion')
                                                # print("complexion : " + complexion[1])
                                                data_dict['complexion'] = complexion[1].strip()
                                            except Exception:
                                                pass

                                            try:
                                                buildCharacteristic = data1.split('Build')
                                                # print("buildCharacteristic : " + buildCharacteristic[1])
                                                data_dict['buildCharacteristic'] = buildCharacteristic[1].strip()
                                            except Exception:
                                                pass

                                    except Exception:
                                        pass

                                    try:
                                        summary = fullName + " is a wanted fugitive listed by FBI"
                                    except Exception:
                                        pass

                                    data_dict['additionalInfo'] = additionalInfo
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

                            driver.back()

                        except Exception:
                            pass

                        j += 1

                except Exception:
                    pass

        except Exception:
            pass

        driver.back()

    # print(len(data_list))
    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    print(data_list)
