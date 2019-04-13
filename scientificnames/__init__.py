import re


def intraspecific_rank(rank):
    return (
        r'(?P<' + rank + r'>'  # group named <rank> can be ...
        r'(?<=' + rank + r'\.\s)\w+'  # a word preceeded by <rank> + dot
        r')'
    )


def skip_rank_specifier(exception):
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
    f'{skip_rank_specifier("subsp")}'
    f'{intraspecific_rank("subsp")}?'
    f'{skip_rank_specifier("var")}'
    f'{intraspecific_rank("var")}?'
    f'{skip_rank_specifier("f")}'
    f'{intraspecific_rank("f")}?'
    r'.*'
    r'$'
)


def parse(scientific_name):
    return re.match(pattern, scientific_name)
