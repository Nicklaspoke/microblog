#!/bin/sh

python -m venv .venv

. .venv/bin/activate

pip3 install -r requirements/test.txt

python3 -m coverage run --rcfile=.coveragerc -m py.test -c pytest.ini tests/unit

make validate