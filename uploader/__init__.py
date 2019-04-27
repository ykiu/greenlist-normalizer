from requests import post

from paths import (
    normalized_taxon_path,
    normalized_common_name_path,
    normalized_scientific_name_path,
)


def upload(url, taxonomy_id, token):
    with normalized_taxon_path.open('rb') as tx_fp, \
            normalized_common_name_path.open('rb') as cn_fp, \
            normalized_scientific_name_path.open('rb') as sn_fp:
        response = post(
            url,
            data={
                'taxonomy': taxonomy_id,
            },
            files={
                'taxa': tx_fp,
                'common_names': cn_fp,
                'scientific_names': sn_fp,
            },
            headers={
                'authorization': f'jwt {token}'
            },
        )
        print(response.json())
