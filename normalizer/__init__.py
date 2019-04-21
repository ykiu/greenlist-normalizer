import unicodedata
from contextlib import contextmanager
from pathlib import Path
from collections import namedtuple
from itertools import groupby, chain
from csv import DictWriter, DictReader


from keygenerator import generate_key

fern_source_path = Path('downloader/csv/FernGreenListV1.01.csv')
angiosperm_source_path = Path('downloader/csv/GreenListAv1.01.csv')
gymnosperm_source_path = Path('downloader/csv/GymGreenListv1.0.csv')

taxon_dest_path = Path('normalizer/normalized/taxa.csv')
common_name_dest_path = Path('normalizer/normalized/common_names.csv')
scientific_name_dest_path = Path('normalizer/normalized/scientific_names.csv')


def get_genus(string):
    return string.split()[0]


def dump(taxon_fp, cn_fp, sn_fp, taxa):
    taxon_writer = DictWriter(taxon_fp, ['parent_key', 'key', 'sort_key'])
    taxon_writer.writeheader()
    cn_writer = DictWriter(cn_fp, ['taxon_key', 'name'])
    cn_writer.writeheader()
    sn_writer = DictWriter(sn_fp, ['taxon_key', 'name'])
    sn_writer.writeheader()

    for taxon in taxa:
        taxon_writer.writerow({
            'parent_key': taxon.parent_key,
            'key': taxon.key,
            'sort_key': taxon.sort_key
        })
        for common_name in taxon.common_names:
            cn_writer.writerow({
                'taxon_key': taxon.key,
                'name': common_name
            })
        for scientific_name in taxon.scientific_names:
            sn_writer.writerow({
                'taxon_key': taxon.key,
                'name': scientific_name
            })


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
    synonym_delimiter='ï¼Œ',
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
        family_sns = family_sn.split('/')
        family_key = family_sns[0].lower()
        yield Taxon(
            parent_key=root_key,
            key=family_key,
            sort_key=sort_key,
            common_names=[family_cn],
            scientific_names=family_sns,
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


def normalize_dictcontent(the_dict):
    '''Normalize those evil full-width ('全角') characters'''
    return {
        k: unicodedata.normalize('NFKC', v) for k, v in the_dict.items()
    }


class TaxonReader:
    def __init__(self, path, **kwargs):
        self.path = path
        self.kwargs = kwargs

    @contextmanager
    def __call__(self):
        with self.path.open(
                encoding='utf8', newline='') as fp:
            csv_reader = DictReader(fp)
            normalized_csv_rows = map(normalize_dictcontent, csv_reader)
            yield rows_to_taxa(
                rows=normalized_csv_rows,
                **self.kwargs
            )


read_angiosperms = TaxonReader(
    angiosperm_source_path,
    sp_common_name_colname='新リスト和名',
    sp_common_name_syn_colname='和名異名',
    sp_scientific_name_colname='GreenList学名',
    fa_common_name_colname='APG科和名',
    fa_scientific_name_colname='APG科名',
    root_key='magnoliophyta',
    synonym_delimiter='，',
)


read_gymnosperms = TaxonReader(
    gymnosperm_source_path,
    sp_common_name_colname='GreenList和名',
    sp_common_name_syn_colname='GreenList和名別名',
    sp_scientific_name_colname='GreenList学名',
    fa_common_name_colname='APG科和名',
    fa_scientific_name_colname='APG科名',
    root_key='ginkgophyta',
    synonym_delimiter=', ',
)


read_ferns = TaxonReader(
    fern_source_path,
    sp_common_name_colname='新リスト和名',
    sp_common_name_syn_colname='和名異名',
    sp_scientific_name_colname='GreenList学名',
    fa_common_name_colname='PPG科和名',
    fa_scientific_name_colname='PPG科名',
    root_key='pteridophyta',
    synonym_delimiter='，',
)


def open_to_write(path):
    return path.open('w', encoding='utf8', newline='')


def normalize_all():
    with read_angiosperms() as angiosperms_artifacts, \
            read_gymnosperms() as gymnosperms_artifacts, \
            read_ferns() as ferns_artifacts:
        root_artifacts = [
            Taxon('tracheophytes', 'pteridophyta', 0,
                  ['シダ植物門'], ['Pteridophyta']),
            Taxon('tracheophytes', 'ginkgophyta', 0,
                  ['裸子植物門'], ['Ginkgophyta']),
            Taxon('tracheophytes', 'magnoliophyta', 0,
                  ['被子植物門'], ['Magnoliophyta']),
        ]
        all_artifacts = chain(
            root_artifacts,
            ferns_artifacts,
            gymnosperms_artifacts,
            angiosperms_artifacts,
        )
        with open_to_write(taxon_dest_path) as taxon_fp, \
                open_to_write(common_name_dest_path) as common_name_fp, \
                open_to_write(scientific_name_dest_path) as scientific_name_fp:
            dump(taxon_fp, common_name_fp, scientific_name_fp, all_artifacts)
