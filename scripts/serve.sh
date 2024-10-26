#!/bin/bash

DP_ROOT=$(realpath $(dirname $0)/..)

cd $DP_ROOT

python3 -m http.server 8080 --bind 0.0.0.0
