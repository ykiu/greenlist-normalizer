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
                r'(?!'
                f'{exception}'
                r')'
                for exception in exceptions
            )
        )
        + r'.)*'
    )


SKIP_NOT_INTERESTING = skip_except([
    r'\bsubsp\.\s',
    r'\bvar\.\s',
    r'\bf\.\s'
])


ROOT_PATTERN = (
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
)

pattern = re.compile(ROOT_PATTERN)


def parse(scientific_name):
    return re.match(pattern, scientific_name)
