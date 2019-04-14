from pathlib import Path
from unittest import TestCase
from csv import DictReader


from normalizer import (
    rows_to_taxa,
    Taxon
)


sample_path = Path(__file__).parent.joinpath('sample.csv')


class NormalizerTest(TestCase):

    def setUp(self):
        self._file = sample_path.open('r', encoding='utf8')
        self.reader = DictReader(self._file)

    def tearDown(self):
        self._file.close()

    def test_normal(self):
        expected = [
            Taxon(
                'plants',
                'cabombaceae',
                0,
                ['ジュンサイ科'],
                ['Cabombaceae']
            ),
            Taxon(
                'cabombaceae',
                'brasenia',
                0,
                [],
                ['Brasenia']
            ),
            Taxon(
                'brasenia',
                'brasenia_schreberi',
                0,
                ['ジュンサイ'],
                ['Brasenia schreberi J.F.Gmel.']
            ),
            Taxon(
                'plants',
                'nymphaeaceae',
                1,
                ['スイレン科'],
                ['Nymphaeaceae']
            ),
            Taxon(
                'nymphaeaceae',
                'euryale',
                0,
                [],
                ['Euryale']
            ),
            Taxon(
                'euryale',
                'euryale_ferox',
                0,
                ['オニバス'],
                ['Euryale ferox Salisb.']
            ),
            Taxon(
                'nymphaeaceae',
                'nuphar',
                1,
                [],
                ['Nuphar']
            ),
            Taxon(
                'nuphar',
                'nuphar_japonica',
                0,
                ['コウホネ'],
                ['Nuphar japonica DC.']
            ),
        ]
        actual = [*rows_to_taxa(
            rows=self.reader,
            sp_common_name_colname='新リスト和名',
            sp_common_name_syn_colname='和名異名',
            sp_scientific_name_colname='GreenList学名',
            fa_common_name_colname='APG科和名',
            fa_scientific_name_colname='APG科名',
            root_key='plants',
            synonym_delimiter='，',
        )]
        assert expected == actual, (
            f'\nexpected:\n{expected}\nactual:\n{actual}'
        )
