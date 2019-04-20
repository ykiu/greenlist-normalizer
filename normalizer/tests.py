from io import StringIO
from pathlib import Path
from unittest import TestCase
from csv import DictReader


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
taxa_path = Path('normalizer/testdata/normalized/taxa.csv')
scientific_names_path = Path(
    'normalizer/testdata/normalized/scientific_names.csv')
common_names_path = Path(
    'normalizer/testdata/normalized/common_names.csv')

taxon_artifacts = (
    Taxon('plants', 'cabombaceae', 0, ['ジュンサイ科'], ['Cabombaceae']),
    Taxon('cabombaceae', 'brasenia', 0, [], ['Brasenia']),
    Taxon('brasenia', 'brasenia_schreberi', 0, ['ジュンサイ'], ['Brasenia schreberi J.F.Gmel.']),  # noqa: E501
    Taxon('plants', 'nymphaeaceae', 1, ['スイレン科'], ['Nymphaeaceae']),
    Taxon('nymphaeaceae', 'euryale', 0, [], ['Euryale']),
    Taxon('euryale', 'euryale_ferox', 0, ['オニバス'], ['Euryale ferox Salisb.']),
    Taxon('nymphaeaceae', 'nuphar', 1, [], ['Nuphar']),
    Taxon('nuphar', 'nuphar_japonica', 0, ['コウホネ'], ['Nuphar japonica DC.']),
)


def read_content(path: Path):
    with path.open(encoding='utf8', newline='\r\n') as fp:
        return fp.read()


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
            root_key='plants',
            synonym_delimiter='，',
        ),)
        assert_equal(expected, actual)


class DumpTest(TestCase):
    def test_normal(self):
        taxa_fp = StringIO(newline='')
        common_names_fp = StringIO(newline='')
        scientific_names_fp = StringIO(newline='')
        dump(taxa_fp, common_names_fp, scientific_names_fp, taxon_artifacts)
        actual_taxa = taxa_fp.getvalue()
        actual_common_names = common_names_fp.getvalue()
        actual_scientific_names = scientific_names_fp.getvalue()

        expected_taxa = read_content(taxa_path)
        expected_common_names = read_content(common_names_path)
        expected_scientific_names = read_content(scientific_names_path)
        assert_equal(expected_taxa, actual_taxa)
        assert_equal(expected_common_names, actual_common_names)
        assert_equal(expected_scientific_names, actual_scientific_names)
