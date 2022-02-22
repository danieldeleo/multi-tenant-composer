#!/bin/bash

apt-get install python3-dev python3-venv -y
python3 -m venv venv && source venv/bin/activate
venv/bin/python3 -m pip install -r requirements.txt
PYTHONPATH=/workspace venv/bin/python3 test/validate_dag.py