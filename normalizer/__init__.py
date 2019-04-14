from collections import namedtuple
from itertools import groupby
from csv import DictWriter, DictReader


import exceptions
import scientificnames


def get_genus(string):
    return string.split()[0]


def normalize(
    source_fp,
    taxon_fp,
    cn_fp,
    sn_fp,
    sp_common_name_colname,
    sp_common_name_syn_colname,
    sp_scientific_name_colname,
    fa_common_name_colname,
    fa_scientific_name_colname,
    root_key,
):
    def by_genus(rows):
        return groupby(
            rows,
            lambda x: get_genus(x[sp_scientific_name_colname])
        )

    taxon_writer = DictWriter(taxon_fp, ['parent_key', 'key', 'sort_key'])
    taxon_writer.writeheader()
    cn_writer = DictWriter(cn_fp, ['taxon_key', 'name'])
    cn_writer.writeheader()
    sn_writer = DictWriter(sn_fp, ['taxon_key', 'name'])
    sn_writer.writeheader()

    reader = DictReader(source_fp)
    for genus, rows in by_genus(reader):
        yield {'parent_key': root_key, 'key': genus, 'sort_key': 0}


def generate_key(scientific_name):
    match = scientificnames.parse(scientific_name)
    if not match:
        raise exceptions.UnparsableScientificNameException(
            f'Failed to parse"{scientific_name}"', scientific_name)
    key = '_'.join(item.lower() for item in match.groups() if item is not None)
    return key


Taxon = namedtuple(
    'Taxon',
    ['parent_key', 'key', 'sort_key', 'common_names', 'scientific_names'])


def rows_to_taxa(
    rows,
    sp_common_name_colname,
    sp_common_name_syn_colname,
    sp_scientific_name_colname,
    fa_common_name_colname,
    fa_scientific_name_colname,
    root_key,
    synonym_delimiter='，',
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
        family_key = family_sn.lower()
        yield Taxon(
            parent_key=root_key,
            key=family_key,
            sort_key=sort_key,
            common_names=[family_cn],
            scientific_names=[family_sn],
        )
        for sort_key, (genus_sn, rows) in enumerate(by_genus(rows)):
            genus_key = genus_sn.lower()
            yield Taxon(
                parent_key=family_key,
                key=genus_key,
                sort_key=sort_key,
                common_names=[],
                scientific_names=[genus_sn],
            )
            for sort_key, row in enumerate(rows):
                sp_sn = row[sp_scientific_name_colname]
                species_key = generate_key(sp_sn)
                sp_cn = row[sp_common_name_colname]
                sp_cn_syn = [
                    s for s in row[sp_common_name_syn_colname].split(
                        synonym_delimiter)
                    if s != ''
                ]
                yield Taxon(
                    parent_key=genus_key,
                    key=species_key,
                    sort_key=sort_key,
                    common_names=[sp_cn, *sp_cn_syn],
                    scientific_names=[sp_sn],
                )
