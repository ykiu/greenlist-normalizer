from collections import namedtuple


import scientificnames
import exceptions


Part = namedtuple('Part', ['regex_group_name', 'prefix'])


parts = [
    Part('hybrid_before_gen_0', ''),
    Part('genus_0', ''),
    Part('hybrid_before_sp_0', ''),
    Part('species_0', ''),
    Part('subsp_0', 'subsp_'),
    Part('nothosubsp_0', 'nothosubsp_'),
    Part('var_0', 'var_'),
    Part('nothovar_0', 'nothovar_'),
    Part('subvar_0', 'subvar_'),
    Part('f_0', 'f_'),
    Part('nothof_0', 'nothof_'),
    Part('hybrid_before_gen_1', ''),
    Part('genus_1', ''),
    Part('hybrid_before_sp_1', ''),
    Part('species_1', ''),
    Part('subsp_1', 'subsp_'),
    Part('nothosubsp_1', 'nothosubsp_'),
    Part('var_1', 'var_'),
    Part('nothovar_1', 'nothovar_'),
    Part('subvar_1', 'subvar_'),
    Part('f_1', 'f_'),
    Part('nothof_1', 'nothof_'),
]


def build_segment(prefix, regex_group_content):
    if regex_group_content is None:
        return
    return prefix + regex_group_content


def generate_key(scientific_name):
    match = scientificnames.parse(scientific_name)
    if not match:
        raise exceptions.UnparsableScientificNameException(
            f'Failed to parse"{scientific_name}"', scientific_name)
    groups = match.groupdict().copy()
    segments = (
        build_segment(prefix, groups.pop(group_name))
        for group_name, prefix in parts)
    key = '_'.join(
        segment for segment in segments if segment is not None).lower()
    assert not groups
    return key
