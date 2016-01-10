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
    cd example.dengueviz

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

For this tutorial We will be using a sample dengue cases dataset coming from 
Malaysian Government Open Data, contributed by Ministry of Health Malaysia. 

Let download the file for this tutorial::

    wget https://raw.githubusercontent.com/koslab/pysiphae/master/sample_data/dengue-hotspot.jsonl -O src/example/dengueviz/dengue-hotspot.jsonl

Following are descriptions of each fields in the data

* `year` - year of outbreak
* `week` - the `epidemiological week <http://www.cmmcp.org/epiweek.htm>`_ of
  outbreak
* `locality` - location of outbreak
* `district_zone_pbt` - district/zone/pbt of location
* `state` - state which the location belong in
* `length_of_outbreak_days` - length of outbreak
* `total_accumulated_cases` - total cases in data point

    
Creating A Simple Dashboard
----------------------------

A simple pysiphae dashboard will consist of the following components:

.. graphviz::

   graph components {
        graph [splines=ortho, rankdir=RL];
        node [shape=component];
        browser [shape=ellipse];
        view [label="View"];
        template [label="TAL Template"];
        jsonview [label="JSON View"];
        data [shape=box3d, label="Data Store"];
        js [label="Visualization JS"];
        pysiphae [shape=folder, label="Pysiphae"];
        browser -- template;
        template -- view;
        template -- js;
        js -- jsonview;
        jsonview -- data;
        view -- pysiphae;
        jsonview -- pysiphae;
   }

Transforming Data And Publish as JSON
++++++++++++++++++++++++++++++++++++++

Before starting to develop visualization, we need to prepare our dataset in a
format that can be visualized. For the sake of this tutorial, we are only
interested with date, state, and case count. We also need to publish our data
into JSON or CSV format for the consumption of DC.js visualization library. 

Our dataset come with many fields that we dont need, and come in JSONLines
format. So lets create a view that will do some preprocessing on the data,
transform them and publish as JSON.

.. note::

   While in this tutorial we do our data transformation in a view, it is not
   exactly a good practice to do it this way, especially when you are dealing
   with massive datasets. Best practice is to preprocess your data in your 
   data system first and only load processed/prepared data from your dashboard
   application

By default pysiphae already generated a blank view for your application. We
will use that view for our dashboard elements, while JSON will be published by
a separate view.

First we will need to register a route for the JSON view. Edit
`src/example/dengueviz/routes.zcml` and add these lines:

.. code-block:: xml

   <route name="example.dengueviz.json"
         pattern="/example.dengueviz.json"/>

Edit `src/example/dengueviz/view.py` and add these lines in the `Views` class.

.. code-block:: python

   @view_config(route_name='example.dengueviz.json',
                renderer='json')
   def json_view(self):
       # load data into memory
       f = asset.load('example.dengueviz:dengue-hotspot.jsonl')
       data = [json.loads(l) for l in f]
    
       # select only fields we want
       data = [{'epiweek': d['week'],
                'year': d['year'],
                'state': d['state'].upper(),
                'count': d['total_accumulated_cases']} for d in data]

       # publish
       return data

.. seealso::
   
   `Pyramid Route Pattern Syntax <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html#route-pattern-syntax>`_
        URL Route patterns documentation.

   `Pyramid View <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/views.html>`_
        Pyramid Views documentations. Please take note that Pysiphae uses
        views that are attached to classes.
   
   `Asset <https://pypi.python.org/pypi/asset/>`_
        Asset library documentation.


Registering navigation elements
-------------------------------

Setting dashboard as home view
-------------------------------

