import re


def intraspecific_rank(rank):
    return (
        r'(?P<' + rank + r'>\w+)'
    )


def skip_to_rank_specifier(exception):
    return (
        r'((?<!\s'
        f'{exception}'
        r'\.\s).)*'
    )


pattern = re.compile(
    r'^'
    r'(?P<genus>\w+?)'
    r'\s+'
    r'(?P<species>\w+?)'
    r'\s+'
    f'{skip_to_rank_specifier("subsp")}'
    r'\s*'
    f'{intraspecific_rank("subsp")}?'
    r'\s+'
    f'{skip_to_rank_specifier("var")}'
    r'\s*'
    f'{intraspecific_rank("var")}?'
    r'\s+'
    f'{skip_to_rank_specifier("f")}'
    r'\s*'
    f'{intraspecific_rank("f")}?'
    r'\s+'
    r'.*'
    r'$'
)


def parse(scientific_name):
    return re.match(pattern, scientific_name)
