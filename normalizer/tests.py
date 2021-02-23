from io import StringIO
from pathlib import Path
from unittest import TestCase
from csv import DictReader
import json


from normalizer import (
    rows_to_taxa,
    dump,
    Taxon
)


def assert_equal(expected, actual):
    assert expected == actual, (
        f'\nexpected:\n{expected}\nactual:\n{actual}'
    )


original_path = Path('normalizer/testdata/original.csv')
taxa_path = Path('normalizer/testdata/normalized/taxa.json')

taxon_artifacts = (
    Taxon('/000/', 0, ['ジュンサイ科'], ['Cabombaceae']),
    Taxon('/000/000/', 0, [], ['Brasenia']),
    Taxon('/000/000/000/', 0, ['ジュンサイ'], ['Brasenia schreberi J.F.Gmel.']),
    Taxon('/001/', 1, ['スイレン科'], ['Nymphaeaceae']),
    Taxon('/001/000/', 0, [], ['Euryale']),
    Taxon('/001/000/000/', 0, ['オニバス'], ['Euryale ferox Salisb.']),
    Taxon('/001/001/', 1, [], ['Nuphar']),
    Taxon('/001/001/000/', 0, ['コウホネ'], ['Nuphar japonica DC.']),
)


class RowsToTaxaTest(TestCase):

    def setUp(self):
        self._file = original_path.open('r', encoding='utf8')
        self.reader = DictReader(self._file)

    def tearDown(self):
        self._file.close()

    def test_normal(self):
        expected = taxon_artifacts
        actual = (*rows_to_taxa(
            rows=self.reader,
            sp_common_name_colname='新リスト和名',
            sp_common_name_syn_colname='和名異名',
            sp_scientific_name_colname='GreenList学名',
            fa_common_name_colname='APG科和名',
            fa_scientific_name_colname='APG科名',
        ),)
        assert_equal(expected, actual)


class DumpTest(TestCase):
    def test_normal(self):
        taxa_fp = StringIO(newline='')
        dump(taxa_fp, taxon_artifacts)
        taxa_fp.seek(0)
        actual_taxa = json.load(taxa_fp)

        with taxa_path.open(encoding='utf8') as fp:
            expected_taxa = json.load(fp)

        assert_equal(expected_taxa, actual_taxa)
