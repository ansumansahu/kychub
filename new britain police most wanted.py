'''
Month_assigned : April
Date Submitted : 26-04-2022
Date_source_name : new britain police most wanted
Harvesting_URL : http://www.newbritainpolice.org/images/arrest_warrant_list.pdf
Data_Extractor : Ansuman Sahu
'''


import hashlib
import json
import csv
import time
import tabula
import requests


def to_json(data_list):
    hash_obj = json.dumps(data_list)
    with open('json/dictionary.json', 'w') as ts:
        ts.write(hash_obj)


def get_hash_of_html(html_string):
    hash_object = hashlib.md5(html_string.encode('utf-8'))
    hash_of_html = hash_object.hexdigest()
    return hash_of_html


def get_data(slug_name):
    data_list = []
    last_updated_dev = int(time.time())
    update_label_ts = int(time.time())

    # convert PDF into CSV
    tabula.convert_into("C:/Users/Ansh/Downloads/arrest_warrant_list.pdf", "arrest_warrant_list", output_format="csv", pages='all')

    file = open("arrest_warrant_list")
    csvreader = csv.reader(file)
    for row in csvreader:
        if row[3] and (row[0] != 'Incident Number'):
            data_dict = {}
            fullName = row[1]
            temp = row[3].split('-')
            data_dict['fullName'] = fullName
            data_dict['age'] = temp[0].strip()
            data_dict['dob'] = temp[1].strip()
            data_dict['fullAddress'] = row[2]
            data_dict['category'] = 'CRIME'
            data_dict['additionalInfo'] = "Incident Number: " + row[0]
            data_dict['summary'] = 'New Britain Police Department has issued warrant for ' + fullName
            # print(data_dict)
            html_hash = get_hash_of_html(str(data_dict))
            data_dict['UpdationFlag'] = True
            data_dict['RawHtml'] = html_hash
            data_dict['LastUpdatedDev'] = last_updated_dev
            data_dict['UpdateLabelTs'] = update_label_ts

            if data_dict:
                data_list.append(data_dict)

    file.close()

    return data_list


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    # to_json(data_list)
    # print(len(data_list))
