#!/bin/bash

apt-get install python3-venv -y
python3 -m venv venv && source venv/bin/activate
venv/bin/python -m pip install -r requirements.txt
PYTHONPATH=/workspace venv/bin/python test/validate_dag.py