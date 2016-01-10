Tutorial: Building A Dengue Visualization Dashboard
=====================================================

.. warning::

   Pysiphae API is still under experimentation and development, and there is
   no API stability promised at the moment. Do not use this for production
   unless you know what you are doing.

Following is a general flow for developing a visualization dashboard
on Pysiphae

.. graphviz::

   digraph Flow {
        graph [splines=ortho, rankdir=LR];
        node [shape=box];
        start [shape=circle];

        has_env [shape=diamond, label="Installed\nPysiphae"];
        installenv [label="Setup\nEnvironment"];
        create_skel [label="Create\nSkeleton"];
        prep_data [label="Prepare\nData"];
        create_view [label="Create\nView"];
        create_dashboard [label="Create\nDashboard"];
        deploy [shape=circle];
        buildout [label="Buildout"];
        start -> has_env;
        has_env -> create_skel [label="Yes"];
        has_env -> installenv [label="No"];
        installenv -> create_skel;
        create_skel -> buildout;
        buildout -> prep_data;
        prep_data -> create_view;
        create_view -> create_dashboard;
        create_dashboard -> deploy;
   }


Setting up your environment
----------------------------

Installing Pysiphae
++++++++++++++++++++

To install pysiphae, run::

    pip install git+https://github.com/koslab/pysiphae.git

.. note:: 

   this method of installation is only recommended at the current state of
   development, once the first release is available in pypi.python.org, please
   install from there.

After installation, you should be getting `templer` command installed. Templer
is a code template generator created by Plone community, based on Python Paste.
You can invoke this command to generate your first Pysiphae project.


.. seealso::

   Virtualenv:
     Ideally you should use a virtualenv to install pysiphae. Refer:
     http://docs.python-guide.org/en/latest/dev/virtualenvs/

   Templer Documentation:
     http://templer-manual.readthedocs.org/en/latest/

Creating Your First Pysiphae Project
+++++++++++++++++++++++++++++++++++++

Once you have templer with pysiphae installed, you can initialize your project
using::

    templer pysiphae example.dengueviz

.. note::

   `example.dengueviz` is your project name. You may change the name to a
   different one

After creating the template, let build it dependencies. A `build.sh` script is
included in your template to simplify the build process::

    bash -e build.sh

.. note::

   You will need the following system dependencies to build pysiphae
   successfully on a Fedora/CentOS/RHEL systems. On debian based systems,
   please install their equivalent

   * python-devel
   * mysql-devel
   * cyrus-sasl-devel
   * openldap-devel
   * gcc-c++
   * python-virtualenv
   * npm

   You will also need to install bower::

     sudo npm install -g bower

.. warning::

   At the current state, the project template uses pysiphae master from github, 
   which is not recommended for production use. This will be changed after our
   first official release.

Getting dataset
----------------

.. todo::
   
   document steps to get sample data here

Creating a dashboard view
--------------------------

Registering navigation elements
-------------------------------

Setting dashboard as home view
-------------------------------

