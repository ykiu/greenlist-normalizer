import unittest
import json
import scientificnames
from pathlib import Path


class ScientificNameTest(unittest.TestCase):

    expectations_path = Path(__file__).parent.joinpath('testexpectations.json')

    @classmethod
    def setUpClass(cls):
        with cls.expectations_path.open('r') as fp:
            cls.expectations = json.load(fp)

    def test_normal(self):
        for msg, original, expected_groups in self.expectations:
            with self.subTest(msg=msg, original=original):
                actual = scientificnames.parse(original)
                self.assertIsNotNone(actual)
                actual_groups = actual.groupdict()
                self.assertEqual(expected_groups, actual_groups)
