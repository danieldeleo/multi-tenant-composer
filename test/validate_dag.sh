#!/bin/bash

python -m pip install -r requirements.txt
PYTHONPATH=/workspace python test/validate_dag.py