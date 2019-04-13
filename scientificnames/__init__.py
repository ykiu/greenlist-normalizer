import re


def intraspecific_rank(rank):
    return (
        r'(?P<' + rank + r'>'  # group named <rank> can be ...
        r'(?<=' + rank + r'\.\s)\w+'  # a word preceeded by <rank> + dot
        r')'
    )


def skip_rank_specifier(exception):
    return (
        r'((?<!\b'
        f'{exception}'
        r'\.\b).)*'
    )


pattern = re.compile(
    r'^'
    r'(?P<genus>\w+?)'
    r'\s+'
    r'(?P<species>\w+?)'
    r'\s+'
    f'{skip_rank_specifier("subsp")}'
    r'\s+'
    f'{intraspecific_rank("subsp")}?'
    r'\s+'
    f'{skip_rank_specifier("var")}'
    r'\s+'
    f'{intraspecific_rank("var")}?'
    r'\s+'
    f'{skip_rank_specifier("f")}'
    r'\s+'
    f'{intraspecific_rank("f")}?'
    r'\s+'
    r'.*'
    r'$'
)


def parse(scientific_name):
    return re.match(pattern, scientific_name)
