'''
Month_assigned : April
Date Submitted : 19-04-2022
Date_source_name : mendocino county most wanted
Data_source_URL : https://www.mendocinocounty.org/government/mendocino-sheriff/news-alerts/most-wanted-mendocino-county
Data_Extractor : Ansuman Sahu
Assinged_cleaner : --
'''

from functools import reduce
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


def get_data(slug_name):
    last_updated_dev = int(time.time())
    update_label_ts = int(time.time())

    url = 'https://www.mendocinocounty.org/government/mendocino-sheriff/news-alerts/most-wanted-mendocino-county'
    data_list = []
    soup = get_soup(url)

    text = soup.text
    temp = text.split('For the F.B.I.\'s Most Wanted List, click here.')[1]
    temp2 = temp.split('###')[:-1]
    for i in temp2:
        temp3 = i.replace('\xa0', '').replace('\r', '')
        li = [i for i in temp3.split('\n') if i]
        data_dict = {}
        fullName = li[0]
        data_dict['fullName'] = fullName
        li2 = li[1:]
        additionalInfo = ''
        for line in li2:
            if 'Date of Birth:' in line or 'DOB:' in line:
                dob = line.replace('Date of Birth:', '').replace('DOB:', '').strip()
                data_dict['dob'] = dob
            elif 'Height:' in line:
                height = line.replace('Height:', '').strip()
                data_dict['height'] = height
            elif 'Weight:' in line:
                weight = line.replace('Weight:', '').strip()
                data_dict['weight'] = weight
            elif 'Aliases:' in line:
                alias = line.replace('Aliases:', '').strip()
                data_dict['alias'] = alias
            elif 'Nickname:' in line:
                additionalInfo = line.strip()
            elif 'Gender:' in line:
                gender = line.replace('Gender:', '').strip()
                data_dict['gender'] = gender
            elif 'Eye Color:' in line:
                eyes = line.replace('Eye Color:', '').strip()
                data_dict['eyes'] = eyes
            elif 'Hair Color:' in line:
                hair = line.replace('Hair Color:', '').strip()
                data_dict['hair'] = hair
            else:
                additionalInfo += " " + line.strip()

        data_dict['category'] = 'Individual'
        data_dict['state'] = 'California'
        data_dict['country'] = 'United States'
        data_dict['additionalInfo'] = additionalInfo
        data_dict['summary'] = 'The individual is a Most Wanted criminal as listed by the County of Mendocino, California, U.S'
        html_hash = get_hash_of_html(str(data_dict))
        data_dict['UpdationFlag'] = True
        data_dict['RawHtml'] = html_hash
        data_dict['LastUpdatedDev'] = last_updated_dev
        data_dict['UpdateLabelTs'] = update_label_ts
        data_list.append(data_dict)

    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    to_json(data_list)
    print(data_list)
