import csv
from pathlib import Path


import xlrd
import requests
from paths import (
    greenlist_url,
    csv_path,
    xls_path,
    basenames_by_taxon_names
)


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
    Path(csv_path).mkdir(exist_ok=True, parents=True)
    Path(xls_path).mkdir(exist_ok=True, parents=True)
    for base_filename in basenames_by_taxon_names.values():
        url = greenlist_url + base_filename + '.xls'
        with xls_path.joinpath(base_filename + '.xls').open('wb') as xlsfile,\
                csv_path.joinpath(base_filename + '.csv').open(
                     'w', newline='', encoding='utf8') as csvfile:
            download_xls_as_csv(url, xlsfile, csvfile)
