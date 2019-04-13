import re


def word(name):
    return r'(?P<' + name + r'>[^\s]+)\b'


def intraspecific_rank(rank):
    return (
        r'(?:' + rank + r'\.\s+(?P<' + rank + r'>[^\s]+))'
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


def normal_name(suffix):
    genus = word('genus' + suffix)
    is_hybrid = r'(?P<' + 'is_hybrid' + suffix + r'>x?)\b'
    species = word('species' + suffix)
    subsp = intraspecific_rank('subsp' + suffix)
    var = intraspecific_rank('var' + suffix)
    f = intraspecific_rank('f' + suffix)
    return (
        r'^'
        f'{genus}'
        r'\s*'
        f'{is_hybrid}'
        r'\s*'
        f'{species}'
        r'\s*'
        f'{SKIP_NOT_INTERESTING}'
        r'\s*'
        f'{subsp}?'
        r'\s*'
        f'{SKIP_NOT_INTERESTING}'
        r'\s*'
        f'{var}?'
        r'\s*'
        f'{SKIP_NOT_INTERESTING}'
        r'\s*'
        f'{f}?'
    )


ROOT_PATTERN = normal_name('')

pattern = re.compile(ROOT_PATTERN)


def parse(scientific_name):
    return re.match(pattern, scientific_name)
