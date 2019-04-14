import csv
from pathlib import Path


import xlrd
import requests


GREENLIST_URL = 'http://www.rdplants.org/gl/'
BASE_FILENAMES = [
    'FernGreenListV1.01',
    'GreenListAv1.01',
    'GymGreenListv1.0'
]
CSV_PATH = 'greenlist/csv/'
XLS_PATH = 'greenlist/xls/'


def download_xls_as_csv(url, xlsfile, csvfile):
    response = requests.get(url)
    xlsfile.write(response.content)
    book = xlrd.open_workbook(xlsfile.name)
    sheet = book.sheet_by_index(0)
    rows = (sheet.row_values(index) for index in range(sheet.nrows))
    csv_writer = csv.writer(csvfile)
    for row in rows:
        csv_writer.writerow(row)


def download_all():
    Path(CSV_PATH).mkdir(exist_ok=True)
    Path(XLS_PATH).mkdir(exist_ok=True)
    for base_filename in BASE_FILENAMES:
        url = GREENLIST_URL + base_filename + '.xls'
        with open(XLS_PATH + base_filename + '.xls', 'wb') as xlsfile,\
                open(CSV_PATH + base_filename + '.csv',
                     'w', newline='', encoding='utf8') as csvfile:
            download_xls_as_csv(url, xlsfile, csvfile)
