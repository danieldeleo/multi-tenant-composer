#!/bin/bash

pip3 install --upgrade pip3
pip3 install -r requirements.txt
PYTHONPATH=/workspace python3 test/validate_dag.py