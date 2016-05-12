Dependencies
===========

* python-devel
* mysql-devel
* cyrus-sasl-devel
* openldap-devel
* gcc-c++
* python-virtualenv
* npm
* bower (sudo npm install -g bower)

Installation
==============

::

    virtualenv venv
    cd venv
    ./bin/pip install git+https://github.com/koslab/pysiphae.git


Creating a dash plugin project
==============================

Initialize::

    ./bin/templer pysiphae mynamespace.myproject
    cd mynamespace.myproject/
    bash -e build.sh

Start development server::

    ./bin/pserve development.ini

Detail Documentation
====================

http://pysiphae.readthedocs.io/en/latest/
