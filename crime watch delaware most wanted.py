'''
Month_assigned : April
Date Submitted : 28-04-2022
Date_source_name : crime watch delaware most wanted
Data_source_URL : https://delaware.crimewatchpa.com/most-wanted
Data_Extractor : Ansuman Sahu
Assinged_cleaner : --
'''

import re

import requests
import time
from bs4 import BeautifulSoup as bs
import hashlib
# from ..general_utility import get_hash_of_html
# from ..s3_upload import hash_check
from selenium import webdriver
from selenium.webdriver.common.by import By
import json


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


def extract_entity(data_sec, raw_html, slug_name):
    html_hash = get_hash_of_html(raw_html)

    # if not hash_check(html_hash, slug_name):
    if data_sec:
        data_dict = {}
        name = ''
        img = ''
        additionalInfo = ''
        summary = ''
        importantDates = ''
        charges = ''
        age = ''
        dob = ''
        distinguishMarks = ''
        height = ''
        weight = ''
        gender = ''
        race = ''
        hair = ''
        eyes = ''
        lastUpdatedAt = ''

        try:
            link = data_sec.find_element(By.CSS_SELECTOR, 'div.field.field-name-field-warrants.field-type-entityreference.field-label-hidden.field-wrapper a').get_attribute('href')
            driver.execute_script('window.open('');')
            driver.switch_to.window(driver.window_handles[1])
            driver.get(link)
            time.sleep(1)

            try:
                driver.find_element(By.XPATH,'//*[@id="notice-modal-96127"]/div/span').click()
                time.sleep(1)
            except Exception:
                pass

            try:
                div = driver.find_element(By.CSS_SELECTOR,'div.body.field')

                try:
                    ps = div.find_elements(By.CSS_SELECTOR,'p')
                    temp = ''
                    links = ''
                    for p in ps:
                        ele = p.text.strip()
                        if "." in ele:
                            arr = ele.split(".")
                            for ent in arr:
                                if "click here" in ent:
                                    links += ent + ": " + p.find_element(By.CSS_SELECTOR,'a').get_attribute('href') + ", "
                                else:
                                    temp += ent + " "
                        else:
                            temp += ele + " "

                    if links:
                        links = links.strip()[:-1]
                        additionalInfo += "Additional Links: " + links.strip()
                    if temp:
                        summary = temp.strip()
                except Exception:
                    pass

                try:
                    lis = div.find_elements(By.CSS_SELECTOR,'li')
                    for li in lis:
                        if "Date Issued" in li.text:
                            temp = li.text.split(":",1)[-1].strip()
                            if temp:
                                if importantDates:
                                    importantDates += "; " + "Date of Issuing of the Warrant: " + temp
                                else:
                                    importantDates += "Date of Issuing of the Warrant: " + temp
                        else:
                            if additionalInfo:
                                additionalInfo += "; " + li.text
                            else:
                                additionalInfo += li.text
                except Exception:
                    pass

                try:
                    temp = div.find_element(By.CSS_SELECTOR,'h2').text.strip()
                    if temp:
                        if importantDates:
                            importantDates += "; " + temp
                        else:
                            importantDates += temp
                except Exception:
                    pass

            except Exception:
                pass

            try:
                temp = driver.find_element(By.CSS_SELECTOR,'span.date-display-single').text.strip()
                if temp:
                    if importantDates:
                        importantDates += "; " + "Date Issued: " + temp
                    else:
                        importantDates += "Date Issued: " + temp
            except Exception:
                pass

            try:
                temp = driver.find_element(By.CSS_SELECTOR,'div.field.field-name-field-charges.field-type-taxonomy-term-reference.field-label-above.field-wrapper.clearfix').text.strip()
                if temp:
                    temp = temp.split("Charges:",1)[-1].strip()
                    if "\n" in temp:
                        temp = temp.replace("\n","; ")
                    if "  " in temp:
                        temp = re.sub("\s+", " ", temp)
                    charges = temp
            except Exception:
                pass

            try:
                temp = driver.find_element(By.CSS_SELECTOR,'div.field.field-name-field-case-number.field-type-text.field-label-above.field-wrapper').text.strip()
                if temp:
                    if "\n" in temp:
                        temp = temp.replace("\n"," ").strip()
                    if "  " in temp:
                        temp = re.sub("\s+"," ", temp)
                    if additionalInfo:
                        additionalInfo += "; " + temp
                    else:
                        additionalInfo += temp
            except Exception:
                pass

            try:
                temp = driver.find_element(By.CSS_SELECTOR,'div.field.field-name-field-incident-type.field-type-taxonomy-term-reference.field-label-above.field-wrapper.clearfix').text.strip()
                if temp:
                    if "\n" in temp:
                        temp = temp.replace("\n"," ").strip()
                    if "  " in temp:
                        temp = re.sub("\s+"," ", temp)
                    if additionalInfo:
                        additionalInfo += "; " + temp
                    else:
                        additionalInfo += temp
            except Exception:
                pass

            try:
                temp = driver.find_element(By.CSS_SELECTOR,'div.field.field-name-post-date.field-type-ds.field-label-hidden.field-wrapper').text.strip()
                if temp:
                    lastUpdatedAt = temp
                    if importantDates:
                        importantDates += "; " + "Page last updated on: " + temp
                    else:
                        importantDates += "Page last updated on: " + temp
            except Exception:
                pass

            try:
                driver.find_element(By.CSS_SELECTOR,'li.horizontal-tab-button.horizontal-tab-button-1.last a').click()
                time.sleep(1)

                try:
                    temp = driver.find_element(By.CSS_SELECTOR,'div.field.field-name-field-address.field-type-addressfield.field-label-above.field-wrapper').text.strip()
                    if temp:
                        temp = temp.split("Location:",1)[-1].strip()
                        if "\n" in temp:
                            temp = temp.replace("\n"," ").strip()
                        if "  " in temp:
                            temp = re.sub("\s+"," ", temp)

                        if additionalInfo:
                            additionalInfo += "; " + "Location of Arrest: " + temp
                        else:
                            additionalInfo += "Location of Arrest: " + temp
                except Exception:
                    pass
            except Exception:
                pass

            try:
                img = driver.find_element(By.CSS_SELECTOR,'div.field.field-name-field-pictures.field-type-image.field-label-hidden.field-wrapper img').get_attribute('src')
            except Exception:
                pass

            try:
                driver.find_element(By.CSS_SELECTOR,'#node-warrant-full-group-offender li.horizontal-tab-button.horizontal-tab-button-1').click()
                time.sleep(1)

                try:
                    temp = driver.find_element(By.CSS_SELECTOR,'fieldset.group-general.field-group-htab.form-wrapper.horizontal-tabs-pane').text.strip()
                    if "\n" in temp:
                        arr = temp.split("\n")
                        for k in range(len(arr)):
                            ele = arr[k]
                            if ":" in ele:
                                val = arr[k+1]
                                if "Date of Birth" in ele:
                                    # print(ele, "; ", val)
                                    temp = val.strip().split(" ")[0].strip()
                                    if lastUpdatedAt:
                                        age = temp
                                        dob = str(int(lastUpdatedAt.split(",")[-1].strip()) - int(temp.strip()))
                                else:
                                    name += val + " "
                    # print(name)
                except Exception:
                    pass

                try:
                    driver.find_element(By.CSS_SELECTOR,'li.horizontal-tab-button.horizontal-tab-button-2.last a').click()
                    time.sleep(1)

                    try:
                        temp = driver.find_element(By.CSS_SELECTOR,'fieldset.required-fields.group-physical-characteristics.field-group-htab.form-wrapper.horizontal-tabs-pane').text.strip()
                        if "\n" in temp:
                            arr = temp.split("\n")
                            for k in range(len(arr)):
                                # print(k, ": ", arr[k].strip())
                                ele = arr[k]
                                if ":" in ele:
                                    val = arr[k+1].strip()

                                    if "Tattoos" in ele:
                                        distinguishMarks = val
                                    elif "Race" in ele:
                                        race = val
                                    elif "Hair" in ele:
                                        hair = val
                                    elif "Eyes" in ele:
                                        eyes = val
                                    elif "Weight" in ele:
                                        weight = val
                                    elif "Height" in ele:
                                        height = val
                                    elif "Gender" in ele:
                                        gender = val
                                    else:
                                        if additionalInfo:
                                            additionalInfo += "; " + ele + val
                                        else:
                                            additionalInfo += ele + val

                    except Exception:
                        pass
                except Exception:
                    pass

            except Exception:
                pass

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
        except Exception:
            pass

        if name:
            summary = name.strip() + " is in the Delaware County's Wanted list." + " " + summary
            data_dict['fullName'] = name.strip()
            data_dict['image'] = img.strip()
            data_dict['charges'] = charges.strip()
            data_dict['gender'] = gender.strip()
            data_dict['dob'] = dob.strip()
            data_dict['age'] = age.strip()
            data_dict['importantDates'] = importantDates.strip()
            data_dict['height'] = height.strip()
            data_dict['weight'] = weight.strip()
            data_dict['race'] = race.strip()
            data_dict['eyes'] = eyes.strip()
            data_dict['distinguishMarks'] = distinguishMarks.strip()
            data_dict['hair'] = hair.strip()
            data_dict['lastUpdatedAt'] = lastUpdatedAt.strip()
            data_dict['additionalInfo'] = additionalInfo.strip()
            data_dict['summary'] = summary.strip()
            data_dict['UpdationFlag'] = True
            data_dict['RawHtml'] = html_hash
            data_dict['LastUpdatedDev'] = last_updated_dev
            data_dict['UpdateLabelTs'] = update_label_ts

        return data_dict
    return {}


def get_data(slug_name):
    url = 'https://delaware.crimewatchpa.com/most-wanted'
    data_list = []
    driver.get(url)
    time.sleep(1)

    try:
        while True:
            try:
                data_secs = driver.find_elements(By.CSS_SELECTOR, 'div.ds-1col.node.node-offender-profile.view-mode-teaser_no_slideshow.interior-content-wrapper.clearfix')
                for data_sec in data_secs:
                    data_dict = extract_entity(data_sec, str(data_sec), slug_name)
                    if data_dict:
                        # print(data_dict)
                        data_list.append(data_dict)

                time.sleep(5)
                driver.find_element(By.XPATH, f'//*[@title="Go to next page"]').click()
                time.sleep(10)
            except Exception:
                break
    except Exception:
        pass

    driver.quit()
    return data_list


if __name__ == "__main__":
    last_updated_dev = int(time.time())
    update_label_ts = int(time.time())

    PATH = "C:\\Users\\Ansh\\Downloads\\Compressed\\chromedriver\\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(options=options, executable_path=PATH)
    data_list = get_data('slug')
    # to_json(data_list)
    # print(data_list)

