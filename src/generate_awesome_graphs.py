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
    existing_branches = {'main'}
    for entry in entries:
        if entry['theme_name'] not in existing_branches:
            gitgraph_text += f'    branch {entry["theme_name"]}\n'
            existing_branches.add(entry['theme_name'])
        gitgraph_text += f'    checkout {entry["theme_name"]}\n'
        gitgraph_text += f'    commit id:\"{entry["id"]}\"\n'

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
