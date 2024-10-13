# Copyright (C) 2024, David Qiu.
"""
Generate awesome list.
"""

import os
import json


def ref2bibstr(ref: dict):
    regular_keys = list(ref.keys())
    regular_keys.remove('ID')
    regular_keys.remove('ENTRYTYPE')

    bibstr = (
        f'@{ref["ENTRYTYPE"]}' + '{' + f'{ref["ID"]}\n' +
        '\n'.join([f'{k} = {ref[k]}' for k in regular_keys]) + '\n' +
        '}'
    )

    return bibstr


def _generate_awesome_list_from_biblist_dict(biblist_dict: dict, level: int) -> str:
    awesome_list_text = ''
    if biblist_dict['title'] is not None:
        awesome_list_text = ('#' * level) + ' ' + biblist_dict['title'] + '\n\n'

    sorted_entries: list = biblist_dict['entries']
    sorted_entries.sort(key=(lambda entry: entry['date']))

    for entry in sorted_entries:
        bibstr = ref2bibstr(entry['ref'])
        awesome_list_text += (
            f'{entry["date"]}\n' +
            f'```\n' +
            f'{bibstr}\n' +
            f'```\n\n'
        )

    for theme_k, subdict in biblist_dict['subthemes'].items():
        awesome_list_text += _generate_awesome_list_from_biblist_dict(subdict, level+1)

    return awesome_list_text


def generate_awesome_list(fp_template: str, fp_data: str, fp_outfile: str) -> str:
    with open(fp_template, 'r') as f:
        template_text = f.read()

    with open(fp_data, 'r') as f:
        data = json.load(f)

    biblist_dict = {'title': None, 'subthemes': {}, 'entries': []}
    for entry_id, entry in data.items():
        leaf_theme = biblist_dict
        for theme_k in entry['theme']:
            if theme_k not in leaf_theme['subthemes']:
                leaf_theme['subthemes'][theme_k] = {'title': theme_k, 'subthemes': {}, 'entries': []}
            leaf_theme = leaf_theme['subthemes'][theme_k]
        leaf_theme['entries'].append(entry)
    
    awesome_list_text = _generate_awesome_list_from_biblist_dict(biblist_dict, level=1)

    output_text = template_text.replace('{{{awesome_list}}}\n', awesome_list_text)

    with open(fp_outfile, 'w') as f:
        f.write(output_text)


def main():
    dp_root = os.path.join(os.path.dirname(__file__), '..')
    generate_awesome_list(
        os.path.abspath(os.path.join(dp_root, 'templates', 'README.md')),
        os.path.abspath(os.path.join(dp_root, 'data', 'data.json')),
        os.path.abspath(os.path.join(dp_root, 'README.md'))
    )
    print('finished generating awesome list..')


if __name__ == '__main__':
    main()
