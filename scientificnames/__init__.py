import re


def intraspecific_rank(rank):
    return (
        r'(?:' + rank + r'\.\s+(?P<' + rank + r'>\w+))'
    )


def skip_except(exceptions):
    return (
        r'('
        + (
            ''.join(
                r'(?!\b'
                f'{exception}'
                r'\.\s)'
                for exception in exceptions
            )
        )
        + r'.)*'
    )


SKIP_NOT_INTERESTING = skip_except(['subsp', 'var', 'f'])


pattern = re.compile(
    r'^'
    r'(?P<genus>\w+?)'
    r'\s+'
    r'(?P<species>\w+?)'
    r'\s+'
    f'{SKIP_NOT_INTERESTING}'
    r'\s*'
    f'{intraspecific_rank("subsp")}?'
    r'\s*'
    f'{SKIP_NOT_INTERESTING}'
    r'\s*'
    f'{intraspecific_rank("var")}?'
    r'\s*'
    f'{SKIP_NOT_INTERESTING}'
    r'\s*'
    f'{intraspecific_rank("f")}?'
    r'\s*'
    r'.*'
    r'$'
)


def parse(scientific_name):
    return re.match(pattern, scientific_name)
