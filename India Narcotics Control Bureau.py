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


def get_data(slug_name):
    last_updated_dev = int(time.time())
    update_label_ts = int(time.time())

    PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver_win32_101\\chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(PATH)
    driver.maximize_window()

    data_list = []
    url = 'https://narcoticsindia.nic.in/'

    driver.get(url)
    time.sleep(1)

    dg_image = driver.find_element(By.XPATH, f"/html/body/div[3]/div[3]/div[2]/div/div/div[1]/div/img").get_attribute('src')
    name_list = []
    image_list = []

    li2 = driver.find_elements(By.XPATH, f'/html/body/div[5]/div/div[2]/div[1]/div/div/div/figure/img')
    for k in range(1, len(li2)+1):
        image = driver.find_element(By.XPATH, f'/html/body/div[5]/div/div[2]/div[1]/div/div[{k}]/div/figure/img').get_attribute('src')
        image_list.append(image)
        name = driver.find_element(By.XPATH, f"/html/body/div[5]/div/div[2]/div[1]/div/div[{k}]/div/h3").text.strip()
        name_list.append(name)

    li = driver.find_elements(By.XPATH, f"/html/body/div[6]/div/div/div[4]/div[2]/div/table/tbody/tr")

    for i in range(1, len(li)+1):
        try:
            data_section = driver.find_elements(By.XPATH, f"/html/body/div[6]/div/div/div[4]/div[2]/div/table/tbody/tr[{i}]")
            for data_sec in data_section:
                if data_sec:
                    data_dict = {}
                    fullName = ''
                    image = ''
                    title = ''
                    designation = ''
                    email = ''
                    summary = ''

                    try:
                        ele = driver.find_element(By.XPATH, f"/html/body/div[6]/div/div/div[4]/div[2]/div/table/tbody/tr[{i}]/td[1]").text.strip()
                        for index,item in enumerate(name_list):
                            if name_list[index] == ele:
                                image = image_list[index]

                        fullName = " ".join(ele.split()[1:])
                        title = ele.split()[0]
                    except Exception:
                        pass

                    try:
                        designation = driver.find_element(By.XPATH, f"/html/body/div[6]/div/div/div[4]/div[2]/div/table/tbody/tr[{i}]/td[2]").text
                    except Exception:
                        pass

                    if designation == "Director General":
                        image = dg_image

                    try:
                        email = driver.find_element(By.XPATH, f"/html/body/div[6]/div/div/div[4]/div[2]/div/table/tbody/tr[{i}]/td[3]").text
                    except Exception:
                        pass

                    try:
                        if title and fullName:
                            summary = title + " " + fullName + " is a member of Narcotics Control Bureau (NCB) which is an Indian intelligence agency under the Ministry of Home Affairs"
                        else:
                            summary = fullName + " is a member of Narcotics Control Bureau (NCB) which is an Indian intelligence agency under the Ministry of Home Affairs"
                    except Exception:
                        pass

                    if fullName:
                        data_dict['fullName'] = fullName
                        data_dict['image'] = image
                        data_dict['title'] = title
                        data_dict['designation'] = designation
                        data_dict['country'] = "India"
                        data_dict['email'] = email
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

    driver.quit()
    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    # print(data_list)