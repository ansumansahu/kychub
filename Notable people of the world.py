'''
Month_assigned : April
Date Submitted : 27-04-2022
Date_source_name : Notable people of the world
Data_source_URL : https://www.britannica.com/more-on-this-day/April-23
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
from selenium.webdriver import ActionChains



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
    # options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(PATH)
    driver.maximize_window()

    data_list = []
    url = 'https://www.britannica.com/more-on-this-day/April-23'
    driver.get(url)
    time.sleep(1)

    while True:
        try:
            driver.find_element(By.XPATH, f'/html/body/main/div/div/div/div[2]/button').click()
            time.sleep(1)
        except Exception:
            break

    soup = get_soup(url)
    data_Sec = soup.find_all('div', {'class': 'card position-relative'})
    for data in data_Sec:
        link = "https://www.britannica.com" + data.find('a')['href']
        soup = get_soup(link)
        data_dict = {}
        fullName = ''
        image = ''
        designation = ''
        aliasTitle = ''
        dob = ''
        works = ''
        familyInfo = ''
        achievements = ''
        additionalInfo = ''
        lastUpdatedAt = ''
        summary = ''

        try:
            fullName = soup.find('h1', {'class': 'mb-0'}).text.strip()
        except Exception:
            pass

        try:
            temp = soup.find('div', {'class': 'card w-100'})
            image = temp.find('img')['src']
            # print(image)
        except Exception:
            pass

        try:
            designation = soup.find('div', {'class': 'topic-identifier font-16 font-md-20'}).text.strip()
        except Exception:
            pass

        try:
            aliasTitle = soup.find('div', {'class': 'caption mt-5 mt-md-0'}).text.strip()
        except Exception:
            pass

        try:
            lastUpdatedAt = soup.find('span', {'class': 'last-updated mt-5'}).text.replace('•', '').replace('Edit History', '').replace('Last Updated:', '').strip()
        except Exception:
            pass

        try:
            summary = soup.find('p', {'class': 'topic-paragraph'}).text.strip()
        except Exception:
            pass

        info = soup.find('div', {'class': 'text-center mt-20'})
        try:
            data_link = "https://www.britannica.com" + info.find('a')['href']
            soup = get_soup(data_link)
            table = soup.find('table', {'class': 'quick-facts-table table font-14'})
            rows = table.find_all('tr')
            for row in rows:
                temp = row.text.replace('\t', '').strip()
                if ('Baptized' in temp) or ('Born' in temp):
                    temp2 = temp.replace('Baptized', '').replace('Born', '').strip()
                    if "•" in temp2:
                        temp3 = temp2.split('•')
                        dob = temp3[0].strip()
                        additionalInfo += "Place of Birth: " + ",".join(temp3[1:])
                    else:
                        dob = temp2
                        additionalInfo += "Place of Birth: ''"
                if 'Died' in temp:
                    additionalInfo += ", Died: " + temp.replace('Died', '').replace('•', ',').strip()
                if 'Notable Works' in temp:
                    works = temp.replace('Notable Works', '').strip()
                if 'Movement / Style' in temp:
                    additionalInfo += ", Style: " + temp.replace('Movement / Style', '').strip()
                if 'Notable Family Members' in temp:
                    familyInfo = temp.replace('Notable Family Members', '').strip()
                if 'Awards And Honors' in temp:
                    achievements = temp.replace('Awards And Honors', '').strip()
                if 'Role In' in temp:
                    additionalInfo += ", Role In: " + temp.replace('Role In', '').strip()
                if 'Movies/Tv Shows (Acted In)' in temp:
                    additionalInfo += ", Movies/Tv Shows (Acted In): " + temp.replace('Movies/Tv Shows (Acted In)', '').strip()
                if 'Title / Office' in temp:
                    additionalInfo += ", Title / Office: " + temp.replace('Title / Office', '').strip()
                if 'Founder' in temp:
                    additionalInfo += ", Founder: " + temp.replace('Founder', '').strip()
                if 'Political Affiliation' in temp:
                    additionalInfo += ", Political Affiliation: " + temp.replace('Political Affiliation', '').strip()
                if 'Subjects Of Study' in temp:
                    additionalInfo += ", Subjects Of Study: " + temp.replace('Subjects Of Study', '').strip()

        except Exception:
            pass

        if fullName:
            data_dict['fullName'] = fullName
            data_dict['image'] = image
            data_dict['designation'] = designation
            data_dict['dob'] = dob
            data_dict['aliasTitle'] = aliasTitle
            data_dict['works'] = works
            data_dict['familyInfo'] = familyInfo
            data_dict['achievements'] = achievements
            data_dict['additionalInfo'] = additionalInfo
            data_dict['summary'] = summary
            data_dict['lastUpdatedAt'] = lastUpdatedAt
            # print(data_dict)
            data_dict['UpdationFlag'] = True
            html_hash = get_hash_of_html(str(data_dict))
            data_dict['RawHtml'] = html_hash
            data_dict['LastUpdatedDev'] = last_updated_dev
            data_dict['UpdateLabelTs'] = update_label_ts

        if data_dict:
            data_list.append(data_dict)

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    # print(data_list)
