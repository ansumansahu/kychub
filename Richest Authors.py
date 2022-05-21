'''
Month_assigned : April
Date Submitted : 01-04-2022
Date_source_name : Richest Authors
Data_source_URL : https://www.celebritynetworth.com/category/richest-celebrities/authors/
Data_Extractor : Ansuman Sahu
Assinged_cleaner : --
'''

import requests
import time
from bs4 import BeautifulSoup as bs
import hashlib

# from ..general_utility import get_hash_of_html
# from ..s3_upload import hash_check
last_updated_dev = int(time.time())
update_label_ts = int(time.time())
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
    date = ''
    month = ''
    year = str(text).split(",")[-1].strip()
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for k in range(len(months)):
        if months[k] in str(text):
            date = str(text).split(months[k])[-1].split(",")[0].strip()
            month = str(k+1)
            if int(date) < 10:
                date = "0" + date
            if int(month) < 10:
                month = "0" + month
            break
    dob = date + "/" + month + "/" + year
    return dob


def extract_entity(data_sec, raw_html, slug_name):
    html_hash = get_hash_of_html(raw_html)

    if data_sec:
        data_dict = {}
        name = ''
        image = ''
        summary = ''
        dob = ''
        nationality = ''
        gender = ''
        additionalInfo = ''
        designation = ''
        pob = ''
        height = ''
        careerInfo = ''
        age = ''
        importantDates = ''

        try:
            link = str(data_sec['href']).strip()
            soup = get_soup(link)

            try:
                name = soup.find('h2',{'class':'title celeb_stats_table_header'}).text.strip()
                if not name:
                    name = soup.find('h1',{'class':'title'}).text.replace("Net Worth","").strip()
            except Exception:
                pass

            try:
                image = soup.find('img',{'class':'image ggnoads lozad'})['data-src']
            except Exception:
                pass

            try:
                table = soup.find('table',{'class':'celeb_stats_table'})
                rows = table.find_all('tr')
                for k in range(len(rows)):
                    ele = str(rows[k].text).strip()
                    if "Net Worth" in ele:
                        additionalInfo += ele.strip() + "; "
                    elif "Place of Birth" in ele:
                        pob = ele.split(":")[-1].strip()
                    elif "Salary" in ele:
                        additionalInfo += ele.strip() + "; "
                    elif "Height" in ele:
                        height = ele.split(":")[-1].strip()
                    elif "Nationality" in ele:
                        nationality = ele.split(":")[-1].strip()
                    elif "Profession" in ele:
                        careerInfo += ele.strip()
                    elif "Gender" in ele:
                        gender = ele.split(":")[-1].strip()
                    elif "Date of Birth" in ele:
                        temp = ele.split(":")[-1].strip()
                        if "(" in temp:
                            age = temp.split("(")[-1].strip()[:2]
                            temp = temp.split("(")[0].strip()
                        if "-" in temp:
                            if "," in temp:
                                importantDates += "Date of Death: " + temp.split("-")[-1].strip()
                                temp = temp.split("-")[0].strip()
                                dob = extract_dob(temp)
                            else:
                                arr2 = temp.split("-")
                                date = arr2[2].strip()
                                month = arr2[1].strip()
                                year = arr2[0].strip()
                                dob = date + "/" + month + "/" + year
                        else:
                            dob = extract_dob(temp)

            except Exception:
                pass

            try:
                summary = soup.find('div',{'id':'single__post_content'}).find('p').text.strip()
            except Exception:
                pass

            try:
                data_div = soup.find('div',{'id':'single__post_content'})
                data_ps = data_div.find_all('p')
                if len(data_ps) > 1:
                    for k in range(1, len(data_ps)):
                        temp = str(data_ps[k].text).strip()
                        if temp:
                            additionalInfo += "Biography: " + temp.strip() + " "
            except Exception:
                pass

            if summary:
                if "Net Worth:" in summary:
                    summary = summary.split("Net Worth:")[-1].strip()
                elif "net worth:" in summary:
                    summary = summary.split("net worth:")[-1].strip()
                elif "net worth and salary:" in summary:
                    summary = summary.split("net worth and salary:")[-1].strip()
        except Exception:
            pass

        if name:
            data_dict['fullName'] = name.strip()
            data_dict['image'] = image.strip()
            data_dict['designation'] = designation.strip()
            data_dict['dob'] = dob.strip()
            data_dict['placeOfBirthCity'] = pob.strip()
            data_dict['importantDates'] = importantDates.strip()
            data_dict['careerInfo'] = careerInfo.strip()
            data_dict['age'] = age.strip()
            data_dict['height'] = height.strip()
            data_dict['gender'] = gender.strip()
            data_dict['nationality'] = nationality.strip()
            data_dict['additionalInfo'] = additionalInfo.strip()
            data_dict['summary'] = summary.strip()
            data_dict['EmployeeName'] = "Ansuman Sahu"
            data_dict['UpdationFlag'] = True
            data_dict['RawHtml'] = html_hash
            data_dict['LastUpdatedDev'] = last_updated_dev
            data_dict['UpdateLabelTs'] = update_label_ts
            print(data_dict)

        return data_dict
    return {}


def get_data(slug_name):
    url = 'https://www.celebritynetworth.com/category/richest-celebrities/authors/'
    data_list = []
    soup = get_soup(url)
    while True:
        try:
            data_div = soup.find('div', {'id': 'post_listing'})
            data_secs = data_div.find_all('a')
            print(len(data_secs))
            for data_sec in data_secs:
                data_dict = extract_entity(data_sec, str(data_sec), slug_name)
                if data_dict:
                    data_list.append(data_dict)
            data_div = soup.find('div', {'class': 'paginate_buttons navigation main_margin'})
            link_text = str(data_div.find_all('a')[-1].text).strip()

            if not "Previous" in link_text:
                link = data_div.find_all('a')[-1]['href']
                print(link)
                soup = get_soup(link)
            else:
                break

        except Exception:
            break

    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    print(data_list)

