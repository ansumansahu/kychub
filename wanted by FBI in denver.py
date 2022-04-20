'''
Month_assigned : April
Date Submitted : 19-04-2022
Date_source_name : wanted by FBI in denver
Harvesting_URL : https://www.fbi.gov/wanted/additional
Data_Extractor : Ansuman Sahu
'''

import re

import requests
import time
from bs4 import BeautifulSoup as bs
import hashlib
# from ..general_utility import get_hash_of_html
# from ..s3_upload import hash_check

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


def extract_dob(text):
    if not text:
        return text
    dob = ''
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    date = ''
    month = ''
    year = str(text).split(",")[-1].strip()
    for k in range(len(months)):
        if months[k] in str(text):
            date = str(text).split(months[k])[-1].split(",")[0].strip()
            if int(date) < 10:
                date = "0" + date
            if k < 10:
                month = "0" + str(k+1)
            else:
                month = str(k+1)
            break
    dob = date + "/" + month + "/" + year
    return dob


def extract_entity(data_sec, raw_html, slug_name):

    last_updated_dev = int(time.time())
    update_label_ts = int(time.time())

    html_hash = get_hash_of_html(raw_html)

    # if not hash_check(html_hash, slug_name):
    if data_sec:
        data_dict = {}
        name = ''
        img = ''
        summary = ''
        charges = ''
        additionalInfo = ''
        dateOfIncident = ''
        alias = ''
        hair = ''
        eyes = ''
        build = ''
        distinguishMarks = ''
        designation = ''
        nationality = ''
        height = ''
        weight = ''
        dob = ''
        placeOfBirthCity = ''
        race = ''
        gender = ''
        reward = ''

        try:
            name = str(data_sec.text).strip()
        except Exception:
            pass

        try:
            img = str(data_sec.find('img')['src'])
            link = data_sec.find('a')['href']
            soup = get_soup(link)

            try:
                temp = soup.find('p',{'class':'summary'})
                temp = str(temp).split('<p class="summary">')[-1].split("</p>")[0].strip()
                arr = str(temp).split("<br/>")
                # print(arr)
                temp = arr[0]
                flag = 0
                not_acceptables_for_crime = ['Suspicious Death','Deceased Individual','Homicide Victim']
                for ele in not_acceptables_for_crime:
                    if ele in temp:
                        flag = 1
                        if additionalInfo:
                            additionalInfo += "; " + "Type: " + temp
                        else:
                            additionalInfo += "Type: " + temp
                        break
                if flag == 0:
                    charges = temp

                # temp = arr[1]
                if re.search("\d+", arr[1]):
                    dateOfIncident = arr[1].strip()
                    temp = arr[2].strip()
                    if temp:
                        if additionalInfo:
                            additionalInfo += "; " + "Place of Incident: " + temp
                        else:
                            additionalInfo += "Place of Incident: " + temp
                elif re.search("\d+", arr[2]):
                    dateOfIncident = arr[2].strip()
                    temp = arr[1].strip()
                    if temp:
                        if additionalInfo:
                            additionalInfo += "; " + "Place of Incident: " + temp
                        else:
                            additionalInfo += "Place of Incident: " + temp

            except Exception:
                pass

            try:
                poster = soup.find('p',{'class':'screenshot'}).find('img')['src']
                if poster:
                    if additionalInfo:
                        additionalInfo += "; " + "Poster: " + poster
                    else:
                        additionalInfo += "Poster: " + poster
            except Exception:
                pass

            try:
                divs = soup.find_all('div',{'class':'thumbnail-container'})
                add_imgs = ''
                for div in divs:
                    temp = div.find('img')['src']
                    if temp:
                        add_imgs += temp + ", "
                if add_imgs:
                    add_imgs = add_imgs.strip()[:-1]
                    if additionalInfo:
                        additionalInfo += "; " + "Additional Image: " + add_imgs
                    else:
                        additionalInfo += "Additional Image: " + add_imgs
            except Exception:
                pass

            try:
                alias = soup.find('div',{'class':'wanted-person-aliases'}).text.split(":",1)[-1].strip()
            except Exception:
                pass

            try:
                table = soup.find('table',{'class':'table table-striped wanted-person-description'})
                rows = table.find_all('tr')
                for k in range(len(rows)):
                    ele = str(rows[k].text).strip()
                    # print(k, ": ", ele)
                    if "Build" in ele:
                        print(ele)
                        build = ele.split("\n")[-1].strip()
                    elif "Occupation" in ele:
                        designation = ele.split("\n")[-1].strip()
                    elif "Languages" in ele:
                        temp = ele.split("\n")[-1].strip()
                        if temp:
                            if additionalInfo:
                                additionalInfo += "; " + "Languages Known: " + temp
                            else:
                                additionalInfo += "Languages Known: " + temp
                    elif "Scars and Marks" in ele:
                        distinguishMarks = ele.split("\n")[-1].strip()
                    elif "NCIC" in ele:
                        temp = ele.split("\n")[-1].strip()
                        if temp:
                            if additionalInfo:
                                additionalInfo += "; " + "NCIC No.: " + temp
                            else:
                                additionalInfo += "NCIC No.: " + temp
                    elif "Nationality" in ele:
                        nationality = ele.split("\n")[-1].strip()
                    elif "Race" in ele:
                        race = ele.split("\n")[-1].strip()
                    elif "Sex" in ele:
                        gender = ele.split("\n")[-1].strip()
                    elif "Weight" in ele:
                        weight = ele.split("\n")[-1].strip()
                    elif "Height" in ele:
                        height = ele.split("\n")[-1].strip()
                    elif "Eyes" in ele:
                        eyes = ele.split("\n")[-1].strip()
                    elif "Hair" in ele:
                        hair = ele.split("\n")[-1].strip()
                    elif "Place of Birth" in ele:
                        placeOfBirthCity = ele.split("\n")[-1].strip()
                    elif "Date(s) of Birth Used" in ele:
                        temp1 = ele.split("\n")[-1].strip()
                        if len(temp1.split(",")) > 2:
                            temp = temp1.split(",",2)[-1].strip()
                            temp1 = temp1.split(",")[0].strip() + " " + temp1.split(",")[1].strip()
                            if temp:
                                if additionalInfo:
                                    additionalInfo += "; " + "Additional Date of Birth(s): " + temp
                                else:
                                    additionalInfo += "Additional Date of Birth(s): " + temp

                        dob = extract_dob(temp1)
                    else:
                        temp = ele.replace("\n"," ").strip()
                        if additionalInfo:
                            additionalInfo += "; " + temp
                        else:
                            additionalInfo += temp
                        # print()

            except Exception:
                pass

            try:
                reward = soup.find('div',{'class':'wanted-person-reward'}).text.split(":")[-1].strip()
            except Exception:
                pass

            try:
                temp = soup.find('div',{'class':'wanted-person-details'}).text.split(":",1)[-1].replace("\n"," ").strip()
                # print("t1: ",temp)
                if temp:
                    if "\xa0" in temp:
                        temp = temp.replace("\xa0"," ").strip()
                    if "  " in temp:
                        temp = re.sub("\s+"," ", temp).strip()
                    summary += temp.strip()
            except Exception:
                pass

            try:
                temp = soup.find('div',{'class':'wanted-person-remarks'}).text.split(":",1)[-1].replace("\n"," ").strip()
                # print("t1: ",temp)
                if temp:
                    if "\xa0" in temp:
                        temp = temp.replace("\xa0"," ").strip()
                    if "  " in temp:
                        temp = re.sub("\s+"," ", temp).strip()
                    summary += temp.strip()
            except Exception:
                pass

            try:
                temp = soup.find('div',{'class':'wanted-person-caution'}).text.split(":",1)[-1].replace("\n"," ").strip()
                # print("t2: ", temp)
                if "\xa0" in temp:
                    temp = temp.replace("\xa0", " ").strip()
                if temp:
                    if "  " in temp:
                        temp = re.sub("\s+"," ", temp).strip()
                    summary += " " + temp.strip()
            except Exception:
                pass

            try:
                temp = soup.find('div',{'class':'wanted-person-submit'}).text.split(":")[-1].split("Submit an anonymous Tip online")[0].replace("\n"," ").strip()
                if temp:
                    if "\xa0" in temp:
                        temp = temp.replace("\xa0"," ").strip()
                    if "  " in temp:
                        temp = re.sub("\s+"," ", temp).strip()
                    if additionalInfo:
                        additionalInfo += "; Submit a Tip: " + temp
                    else:
                        additionalInfo += "Submit a Tip: " + temp
            except Exception:
                pass

            try:
                temp = soup.find('div',{'class':'wanted-person-warning panel'}).text.strip()
                # print("t3: ", temp)
                if temp:
                    if "\xa0" in temp:
                        temp = temp.replace("\xa0"," ").strip()
                    summary += " " + name.strip() + " " + temp.lower()
            except Exception:
                pass

        except Exception:
            pass

        if name:
            if not summary:
                summary = name.strip() + " is one of the Most Wanted fugitives by FBI in Denver."
            data_dict['fullName'] = name.strip()
            data_dict['image'] = img.strip()
            data_dict['alias'] = alias.strip()
            data_dict['dateOfIncident'] = dateOfIncident.strip()
            data_dict['charges'] = charges.strip()
            data_dict['reward'] = reward.strip()
            data_dict['gender'] = gender.strip()
            data_dict['nationality'] = nationality.strip()
            data_dict['designation'] = designation.strip()
            data_dict['dob'] = dob.strip()
            data_dict['placeOfBirthCity'] = placeOfBirthCity.strip()
            data_dict['height'] = height.strip()
            data_dict['weight'] = weight.strip()
            data_dict['race'] = race.strip()
            data_dict['eyes'] = eyes.strip()
            data_dict['build'] = build.strip()
            data_dict['distinguishMarks'] = distinguishMarks.strip()
            data_dict['hair'] = hair.strip()
            data_dict['additionalInfo'] = additionalInfo.strip()
            data_dict['summary'] = summary.strip()
            data_dict['UpdationFlag'] = True
            data_dict['RawHtml'] = html_hash
            data_dict['LastUpdatedDev'] = last_updated_dev
            data_dict['UpdateLabelTs'] = update_label_ts

        return data_dict
    return {}


def get_data(slug_name):
    url = 'https://www.fbi.gov/wanted/additional'
    data_list = []
    soup = get_soup(url)
    data_secs = soup.find_all('li', {'class': 'portal-type-person castle-grid-block-item'})
    # print(len(data_secs))
    for data_sec in data_secs:
        data_dict = extract_entity(data_sec, str(data_sec), slug_name)
        if data_dict:
            data_list.append(data_dict)
            print(data_dict)
    return data_list


if __name__ == "__main__":
    data_list = get_data('slug')
    # to_json(data_list)
    print(data_list)

