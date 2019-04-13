import re


def word(name):
    return r'(?P<' + name + r'>[^\s]+)\b'


def intraspecific_rank(name, rank):
    return (
        r'(?:' + rank + r'\.\s+(?P<' + name + r'>[^\s]+))'
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
    r'\bf\.\s',
    r'\bx\s',
])


def normal_name(suffix):
    genus = word('genus' + suffix)
    is_hybrid = r'(?P<' + 'is_hybrid' + suffix + r'>x?)\b'
    species = word('species' + suffix)
    subsp = intraspecific_rank('subsp' + suffix, 'subsp')
    var = intraspecific_rank('var' + suffix, 'var')
    f = intraspecific_rank('f' + suffix, 'f')
    return (
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
        r'\s*'
        f'{SKIP_NOT_INTERESTING}'
    )


ROOT_PATTERN = (
    r'^'
    f'{normal_name("_0")}'
)

pattern = re.compile(ROOT_PATTERN)


def parse(scientific_name):
    return re.match(pattern, scientific_name)
