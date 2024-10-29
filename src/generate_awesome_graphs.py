# Copyright (C) 2024, David Qiu.
"""
Generate awesome graphs.
"""

import os
import json


def generate_gitgraph(fp_template: str, fp_data: str, fp_outfile: str) -> str:
    with open(fp_template, 'r') as f:
        template_text = f.read()

    with open(fp_data, 'r') as f:
        data = json.load(f)

    entries = []
    for entry_id, entry in data.items():
        theme_name = '/'.join(entry['theme'])
        entry['id'] = entry_id
        entry['theme_name'] = theme_name or 'main'
        entries.append(entry)
    entries.sort(key=(lambda entry: entry['date']))

    gitgraph_text = 'gitGraph:\n'
    gitgraph_text += '    commit id:"(Embodied AI)"\n'
    existing_branches = {'main'}
    for entry in entries:
        gitgraph_text += f'    checkout main\n'
        if entry['theme_name'] not in existing_branches:
            for i, theme in enumerate(entry['theme']):
                theme_name = '/'.join(entry['theme'][:i+1])
                if theme_name not in existing_branches:
                    gitgraph_text += f'    commit id:"({theme})"\n'
                    gitgraph_text += f'    branch {theme_name}\n'
                    existing_branches.add(theme_name)
                gitgraph_text += f'    checkout {theme_name}\n'
        else:
            gitgraph_text += f'    checkout {entry["theme_name"]}\n'
        display_name = entry['id']
        if 'abbrname' in entry and entry['abbrname']:
            display_ref_fields = []
            if 'ref' in entry and 'author' in entry['ref']:
                display_ref_fields.append(entry['ref']['author'].split(',')[0])
            if 'ref' in entry and 'year' in entry['ref']:
                display_ref_fields.append(entry['ref']['year'])
            else:
                display_ref_fields.append(entry['date'].split('-')[0])
            if len(display_ref_fields) > 0:
                display_name = f'{entry["abbrname"]} [{", ".join(display_ref_fields)}]'
            else:
                display_name = f'{entry["abbrname"]}'
        gitgraph_text += f'    commit id:\"{display_name}\"\n'

    output_text = template_text.replace('{{{awesome_graph:gitgraph}}}\n', gitgraph_text)

    with open(fp_outfile, 'w') as f:
        f.write(output_text)


def main():
    dp_root = os.path.join(os.path.dirname(__file__), '..')
    generate_gitgraph(
        os.path.abspath(os.path.join(dp_root, 'templates', 'index.html')),
        os.path.abspath(os.path.join(dp_root, 'data', 'data.json')),
        os.path.abspath(os.path.join(dp_root, 'index.html'))
    )
    print('finished generating gitgraph..')


if __name__ == '__main__':
    main()
