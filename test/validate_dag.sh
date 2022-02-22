#!/bin/bash

python3 -m pip install -r requirements.txt
PYTHONPATH=/workspace python3 test/validate_dag.py