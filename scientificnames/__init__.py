import re


EXTENDED_W = r'[^\s^\.]'  # similar to \w but matches more characters


INTRA_SPECIFIC_RANKS = ['subsp', 'var', 'subvar', 'nothovar', 'f']


SPECIEAL_WORDS = [
    *(rank + r'\.' for rank in INTRA_SPECIFIC_RANKS),
    'x'
]


def word(name):
    return r'(?P<' + name + r'>' + EXTENDED_W + r'+)'


def intraspecific_rank(name, rank):
    return (
        r'(?:' + rank + r'\.\s+' + word(name) + r')'
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


SKIP_NOT_INTERESTING = skip_except(
    r'\b' + word + r'\s'
    for word in SPECIEAL_WORDS
)


def normal_name(suffix):
    genus = word('genus' + suffix) + r'\.?'
    is_hybrid = r'(?P<' + 'is_hybrid' + suffix + r'>x)?\b'
    species = word('species' + suffix)

    intraspecific_ranks = ''.join(
        intraspecific_rank(rank + suffix, rank) + r'?' + SKIP_NOT_INTERESTING
        for rank in INTRA_SPECIFIC_RANKS
    )

    return (
        f'{genus}'
        r'\s*'
        f'{is_hybrid}'
        r'\s*'
        f'{species}'
        f'{SKIP_NOT_INTERESTING}'
        f'{intraspecific_ranks}'
    )


ROOT_PATTERN = (
    r'^'
    f'{normal_name("_0")}'
    r'(?:'
    r'x\s+'
    f'{normal_name("_1")}'
    r')?'
)

pattern = re.compile(ROOT_PATTERN)


def parse(scientific_name):
    return re.match(pattern, scientific_name)
