Installation
==============

::

    pip install templer.core
    pip install git+https://github.com/koslab/pysiphae.git


Creating a dash plugin project
==============================

Initialize::

    templer pysiphae_dashplugin mynamespace.myproject
    cd mynamespace.myproject/
    virtualenv venv/
    ./venv/bin/python bootstrap-buildout.py
    ./bin/buildout -vvvvv

Start development server::

    ./bin/pserve development.ini
