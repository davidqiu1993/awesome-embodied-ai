#!/bin/bash

DP_ROOT=$(realpath $(dirname $0)/..)
DP_SRC=$DP_ROOT/src
FP_VENV_SOURCE=$DP_ROOT/env/bin/activate


function ensure_success() {
    if [[ $? -ne 0 ]]; then
        echo "ERROR: Exception detected."
        exit 1;
    fi
}


cd $DP_ROOT

if [[ ! -f $FP_VENV_SOURCE ]]; then
    pip3 install virtualenv
    python3 -m virtualenv env

    echo $FP_VENV_SOURCE

    if [[ ! -f $FP_VENV_SOURCE ]]; then
        echo "ERROR: Failed to initialize python virtual environment."
        exit 1;
    fi
fi

source $FP_VENV_SOURCE
pip install -r $DP_SRC/requirements.txt

cd $DP_SRC
python update_data_refs.py
python generate_awesome_list.py
