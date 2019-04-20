import json
from pathlib import Path
from unittest import TestCase

from keygenerator import generate_key


class KeyGeneratorTest(TestCase):

    expectations_path = Path('keygenerator/testdata/expectations.json')

    @classmethod
    def setUpClass(cls):
        with cls.expectations_path.open('r') as fp:
            cls.expectations = json.load(fp)

    def test_normal(self):
        for original, expected in self.expectations:
            with self.subTest(original):
                actual = generate_key(original)
                assert expected == actual, (
                    f'\nexpected:\n{expected}\nactual:\n{actual}'
                )
