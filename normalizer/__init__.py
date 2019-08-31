import re
import unicodedata
import json
from contextlib import contextmanager
from collections import namedtuple
from itertools import groupby, chain
from csv import DictReader

import scientificnames
from keygenerator import generate_key
from paths import (
    fern_csv_path,
    angiosperm_csv_path,
    gymnosperm_csv_path,
    normalized_taxon_path,
)

from normalizer.overrides import (
    sp_key_overrides,
    angiosperm_overrides,
)


def get_genus(string):
    return scientificnames.parse(string).group('genus_0')


def dump(taxon_fp, taxa):
    taxa_json = [{
        'path': taxon.path,
        'sort_key': taxon.sort_key,
        'common_names': [
            {'name': name} for name in taxon.common_names
        ],
        'scientific_names': [
            {'name': name} for name in taxon.scientific_names
        ],
    } for taxon in taxa]
    json.dump({"taxa": taxa_json}, taxon_fp, ensure_ascii=False)


Taxon = namedtuple(
    'Taxon',
    ['path', 'sort_key', 'common_names', 'scientific_names'])


def normalize_family_name(family_name: str):
    cleaned_family_name = re.sub(r'\*', '', family_name)
    split_fn = cleaned_family_name.split('/')
    return split_fn


def normalize_common_name(common_name: str):
    cleaned_cn = re.sub(r'[\(\[「].*?[\)\]」]|\'|自生\?', '', common_name)
    split_cn = [s.strip() for s in re.split(r'[\.\,。、]', cleaned_cn)]
    filtered_cn = [s for s in split_cn if s]
    return filtered_cn


def rows_to_taxa(
    rows,
    sp_common_name_colname,
    sp_common_name_syn_colname,
    sp_scientific_name_colname,
    fa_common_name_colname,
    fa_scientific_name_colname,
    root_path='/',
):
    def by_genus(rows):
        return groupby(
            rows,
            lambda x: get_genus(x[sp_scientific_name_colname])
        )

    def by_family(rows):
        return groupby(
            rows,
            lambda x: (
                x[fa_scientific_name_colname],
                x[fa_common_name_colname]
            )
        )

    for sort_key, ((family_sn, family_cn), rows) in enumerate(by_family(rows)):
        family_sns = normalize_family_name(family_sn)
        family_key = family_sns[0].lower()
        yield Taxon(
            path=f'{root_path}{family_key}/',
            sort_key=sort_key,
            common_names=[family_cn],
            scientific_names=family_sns,
        )
        for sort_key, (genus_sn, rows) in enumerate(by_genus(rows)):
            genus_key = genus_sn.lower()
            yield Taxon(
                path=f'{root_path}{family_key}/{genus_key}/',
                sort_key=sort_key,
                common_names=[],
                scientific_names=[genus_sn],
            )
            for sort_key, row in enumerate(rows):
                sp_sn = row[sp_scientific_name_colname]
                sp_key = (
                    sp_key_overrides.get(sp_sn, None)
                    or generate_key(sp_sn))
                sp_cns = normalize_common_name(
                    row[sp_common_name_colname])
                sp_cn_syns = normalize_common_name(
                    row[sp_common_name_syn_colname])
                sp_all_cns = [*sp_cns, *sp_cn_syns]
                if sp_all_cns:
                    yield Taxon(
                        path=f'{root_path}{family_key}/{genus_key}/{sp_key}/',
                        sort_key=sort_key,
                        common_names=sp_all_cns,
                        scientific_names=[sp_sn],
                    )


def normalize_dictcontent(the_dict):
    '''Normalize those evil full-width ('全角') characters'''
    return {
        k: unicodedata.normalize('NFKC', v) for k, v in the_dict.items()
    }


def apply_overrides(rows, overrides):
    for index, row in enumerate(rows):
        try:
            signature, replacements = overrides[index]
        except KeyError:
            yield row
        else:
            assert all(row[k] == v for k, v in signature.items()), \
                f'{row}\ndoes not match:\n{signature}'
            yield from replacements


class TaxonReader:
    def __init__(self, path, overrides, **kwargs):
        self.path = path
        self.kwargs = kwargs
        self.overrides = overrides

    @contextmanager
    def __call__(self):
        with self.path.open(
                encoding='utf8', newline='') as fp:
            csv_reader = DictReader(fp)
            overridden_rows = apply_overrides(csv_reader, self.overrides)
            normalized_csv_rows = map(normalize_dictcontent, overridden_rows)
            yield rows_to_taxa(
                rows=normalized_csv_rows,
                **self.kwargs
            )


read_angiosperms = TaxonReader(
    angiosperm_csv_path,
    overrides=angiosperm_overrides,
    sp_common_name_colname='新リスト和名',
    sp_common_name_syn_colname='和名異名',
    sp_scientific_name_colname='GreenList学名',
    fa_common_name_colname='APG科和名',
    fa_scientific_name_colname='APG科名',
    root_path='/magnoliophyta/',
)


read_gymnosperms = TaxonReader(
    gymnosperm_csv_path,
    overrides={},
    sp_common_name_colname='GreenList和名',
    sp_common_name_syn_colname='GreenList和名別名',
    sp_scientific_name_colname='GreenList学名',
    fa_common_name_colname='APG科和名',
    fa_scientific_name_colname='APG科名',
    root_path='/ginkgophyta/',
)


read_ferns = TaxonReader(
    fern_csv_path,
    overrides={},
    sp_common_name_colname='新リスト和名',
    sp_common_name_syn_colname='和名異名',
    sp_scientific_name_colname='GreenList学名',
    fa_common_name_colname='PPG科和名',
    fa_scientific_name_colname='PPG科名',
    root_path='/pteridophyta/',
)


def open_to_write(path):
    path.parent.mkdir(exist_ok=True, parents=True)
    return path.open('w', encoding='utf8', newline='')


def normalize_all():
    with read_angiosperms() as angiosperms_artifacts, \
            read_gymnosperms() as gymnosperms_artifacts, \
            read_ferns() as ferns_artifacts:
        root_artifacts = [
            Taxon('/pteridophyta/', 0,
                  ['シダ植物門'], ['Pteridophyta']),
            Taxon('/ginkgophyta/', 1,
                  ['裸子植物門'], ['Ginkgophyta']),
            Taxon('/magnoliophyta/', 2,
                  ['被子植物門'], ['Magnoliophyta']),
        ]
        all_artifacts = chain(
            root_artifacts,
            ferns_artifacts,
            gymnosperms_artifacts,
            angiosperms_artifacts,
        )
        with open_to_write(normalized_taxon_path) as tx_fp:
            dump(tx_fp, all_artifacts)
