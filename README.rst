Dependencies
===========

* python-devel
* mysql-devel
* cyrus-sasl-devel
* openldap-devel
* gcc-c++
* python-virtualenv
* npm


Installation
==============

::

    pip install templer.core==1.0b4
    pip install git+https://github.com/koslab/pysiphae.git


Creating a dash plugin project
==============================

Initialize::

    templer pysiphae mynamespace.myproject
    cd mynamespace.myproject/
    virtualenv venv/
    ./venv/bin/python bootstrap-buildout.py
    ./bin/buildout -vvvvv

Install static files::

    cd dev/pysiphae/pysiphae/static
    bower install
    cd ../../../../

Start development server::

    ./bin/pserve development.ini
