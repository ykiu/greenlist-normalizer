from pathlib import Path

greenlist_url = 'http://www.rdplants.org/gl/'

basenames_by_taxon_names = {
    'fern': 'FernGreenListV1.01',
    'angiosperm': 'GreenListAv1.01',
    'gymnosperm': 'GymGreenListv1.0'
}

csv_path = Path('downloads/csv/')
xls_path = Path('downloads/xls/')

fern_csv_path = csv_path.joinpath(
    basenames_by_taxon_names['fern'] + '.csv')
angiosperm_csv_path = csv_path.joinpath(
    basenames_by_taxon_names['angiosperm'] + '.csv')
gymnosperm_csv_path = csv_path.joinpath(
    basenames_by_taxon_names['gymnosperm'] + '.csv')

normalized_taxon_path = Path('normalizations/taxa.csv')
