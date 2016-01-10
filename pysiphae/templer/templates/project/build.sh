#!/bin/bash -e

which bower
which virtualenv
if [ ! -e ./venv/bin/python ];then
    virtualenv venv
fi
./venv/bin/python bootstrap-buildout.py
./bin/buildout -vvv
pushd dev/pysiphae/pysiphae/static
bower install
popd
