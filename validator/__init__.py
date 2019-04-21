import re
import csv
from pathlib import Path


TAXA_PATH = Path('normalizer/normalized/taxa.csv')
COMMON_NAMES_PATH = Path('normalizer/normalized/common_names.csv')
SCIENTIFIC_NAMES_PATH = Path('normalizer/normalized/scientific_names.csv')


COMMA = re.compile(r'\,')


UNALLOWED_PATTERNS = [COMMA]


class ValidationFailed(Exception):
    '''Validation failed'''


class Validator:
    def __init__(self, patterns):
        self.patterns = patterns

    def __call__(self, string):
        for unallowed_pattern in self.patterns:
            if unallowed_pattern.search(string):
                raise ValidationFailed(string)


cn_validator = Validator([COMMA])
sn_validator = Validator([COMMA])


def validate_all():

    with COMMON_NAMES_PATH.open(encoding='utf8', newline='') as cn_fp:
        for row in csv.DictReader(cn_fp):
            cn_validator(row['name'])

    with SCIENTIFIC_NAMES_PATH.open(encoding='utf8', newline='') as sn_fp:
        for row in csv.DictReader(sn_fp):
            sn_validator(row['name'])
