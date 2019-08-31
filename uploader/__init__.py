from requests import post

from paths import (
    normalized_taxon_path,
)


def upload(url, taxonomy_id, token):
    with normalized_taxon_path.open('rb') as tx_fp:
        response = post(
            url,
            data={
                'taxonomy': taxonomy_id,
            },
            files={
                'taxa': tx_fp,
            },
            headers={
                'authorization': f'jwt {token}'
            },
        )
        print(response.json())
