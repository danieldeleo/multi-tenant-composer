#!/bin/bash

python3.8 -m pip install -r requirements.txt
PYTHONPATH=/workspace python3.8 test/validate_dag.py