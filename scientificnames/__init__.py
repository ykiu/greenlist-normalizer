import re


EXTENDED_W = r'[^\s^\.]'  # similar to \w but matches more characters


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


SKIP_NOT_INTERESTING = skip_except([
    r'\bsubsp\.\s',
    r'\bvar\.\s',
    r'\bsubvar\.\s',
    r'\bf\.\s',
    r'\bx\s',
])


def normal_name(suffix):
    genus = word('genus' + suffix) + r'\.?'
    is_hybrid = r'(?P<' + 'is_hybrid' + suffix + r'>x)?\b'
    species = word('species' + suffix)
    subsp = intraspecific_rank('subsp' + suffix, 'subsp')
    var = intraspecific_rank('var' + suffix, 'var')
    subvar = intraspecific_rank('subvar' + suffix, 'subvar')
    f = intraspecific_rank('f' + suffix, 'f')
    return (
        f'{genus}'
        r'\s*'
        f'{is_hybrid}'
        r'\s*'
        f'{species}'
        f'{SKIP_NOT_INTERESTING}'
        f'{subsp}?'
        f'{SKIP_NOT_INTERESTING}'
        f'{var}?'
        f'{SKIP_NOT_INTERESTING}'
        f'{subvar}?'
        f'{SKIP_NOT_INTERESTING}'
        f'{f}?'
        f'{SKIP_NOT_INTERESTING}'
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
