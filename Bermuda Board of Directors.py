'''
Month_assigned : April
Date Submitted : 04-04-2022
Date_source_name : Bermuda board of directors
Data_source_URL : https://www.bma.bm/board-of-directors
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


def get_data(slug_name):
    url = 'https://www.bma.bm/board-of-directors'
    data_list = []
    soup = get_soup(url)

    fullName = []
    designation = []
    additionalInfo = []
    try:
        data_section = soup.find_all('div', {'class': 'right_bod'})

        for data in data_section:
            temp = data.text.replace("\n\n", "\n").replace('\xa0', '').split('\n')
            test_list = [i for i in temp if i]
            test_list[1:3] = [reduce(lambda x, y: x + ", " + y, test_list[1:3])]

            for i in range(0, len(test_list), 3):
                fullName.append(test_list[i])

            for i in range(1, len(test_list), 3):
                designation.append(test_list[i])

            for i in range(2, len(test_list), 3):
                additionalInfo.append(test_list[i])

    except Exception:
        pass

    for i in range(len(fullName)):
        data_dict = {}
        data_dict['fullName'] = fullName[i].strip()
        data_dict['designation'] = designation[i].strip()
        data_dict['country'] = 'Bermuda'
        data_dict['category'] = 'Individual'
        data_dict['additionalInfo'] = additionalInfo[i].strip()
        data_dict['summary'] = fullName[i].strip() + " is a member of the Board of Directors of Bermuda responsible for managing the affairs and business of the BMA and determining the policy objectives and strategy of the Authority."
        print(data_dict)
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
