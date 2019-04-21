import re
import csv
from pathlib import Path


TAXA_PATH = Path('normalizer/normalized/taxa.csv')
COMMON_NAMES_PATH = Path('normalizer/normalized/common_names.csv')
SCIENTIFIC_NAMES_PATH = Path('normalizer/normalized/scientific_names.csv')


SCIENTIFIC_NAME_UNALLOWED = re.compile(
    r'[^\"a-zA-Z_\-\,\s\(\.\)[^\"a-zA-Z_\-\,\s\(\.\)éôüöèó\'áČÅ]')
COMMON_NAME_UNALLOWED = re.compile(r'[^\u30a1-\u30faー被裸子植物門科×]')


class ValidationFailed(Exception):
    '''Validation failed'''


class Validator:
    def __init__(self, patterns):
        self.patterns = patterns

    def __call__(self, string):
        for unallowed_pattern in self.patterns:
            if unallowed_pattern.search(string):
                raise ValidationFailed(string)


cn_validator = Validator([COMMON_NAME_UNALLOWED])
sn_validator = Validator([SCIENTIFIC_NAME_UNALLOWED])


def validate_all():

    with COMMON_NAMES_PATH.open(encoding='utf8', newline='') as cn_fp:
        for row in csv.DictReader(cn_fp):
            cn_validator(row['name'])

    with SCIENTIFIC_NAMES_PATH.open(encoding='utf8', newline='') as sn_fp:
        for row in csv.DictReader(sn_fp):
            sn_validator(row['name'])
