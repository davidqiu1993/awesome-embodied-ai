# Copyright (C) 2024, David Qiu.
"""
Update references in data with bibliographies.
"""

import os
import bibtexparser
import json


def update_data_refs(fp_data: str, fp_bib: str, verbose: bool=False) -> None:
    """
    Update references in data with bibliographies.

    @param fp_data Path to data file.
    @param fp_bib Path to bibliography file.
    @param verbose Whether to print updates.
    """

    with open(fp_bib, 'r') as f:
        bib = bibtexparser.load(f)

    with open(fp_data, 'r') as f:
        data = json.load(f)

    for k in data:
        if k in bib.entries_dict:
            data[k]['ref'] = bib.entries_dict[k]
            if verbose:
                print(f'Updated reference for "{k}"..')

    with open(fp_data, 'w') as f:
        json.dump(data, f, indent=4)

    if verbose:
        print(f'Updates written to "{fp_data}"..')


def main():
    dp_data = os.path.join(os.path.dirname(__file__), '..', 'data')
    update_data_refs(
        os.path.abspath(os.path.join(dp_data, 'data.json')),
        os.path.abspath(os.path.join(dp_data, 'refs.bib')),
        verbose=True
    )


if __name__ == "__main__":
    main()
