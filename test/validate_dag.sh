#!/bin/bash

python3 -m venv venv && source venv/bin/activate
venv/bin/python -m pip install -r requirements.txt
PYTHONPATH=/workspace venv/bin/python test/validate_dag.py