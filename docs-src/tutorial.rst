=====================================================
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
============================

Installing Pysiphae
--------------------

To install pysiphae, run:

.. code-block:: bash

    pip install git+https://github.com/koslab/pysiphae.git

.. note:: 

   this method of installation is only recommended at the current state of
   development, once the first release is available in pypi.python.org, please
   install from there.

After installation, you should be getting ``templer`` command installed. 
Templer is a code template generator created by Plone community, based on 
Python Paste. You can invoke this command to generate your first Pysiphae 
project.


.. seealso::

   Virtualenv:
     Ideally you should use a virtualenv to install pysiphae. Refer:
     http://docs.python-guide.org/en/latest/dev/virtualenvs/

   Templer Documentation:
     http://templer-manual.readthedocs.org/en/latest/

Creating Your First Pysiphae Project
-------------------------------------

Once you have templer with pysiphae installed, you can initialize your project
using:

.. code-block:: bash

   templer pysiphae example.dengueviz
   cd example.dengueviz

.. note::

   ``example.dengueviz`` is your project name. You may change the name to a
   different one

After creating the template, let build it dependencies. A ``build.sh`` script 
is included in your template to simplify the build process:

.. code-block:: bash

   bash -e build.sh

After a successful build, you can start the application server using the
following command:

.. code-block:: bash

   ./bin/pserve development.ini

The server should be running at http://localhost:6543. To stop the server, press ``CTRL+C``

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
================

For this tutorial We will be using a sample dengue cases dataset coming from 
Malaysian Government Open Data, contributed by Ministry of Health Malaysia. 

Let download the file for this tutorial:

.. code-block:: bash

   wget https://raw.githubusercontent.com/koslab/pysiphae/master/sample_data/dengue-hotspot.jsonl \
        -O src/example/dengueviz/dengue-hotspot.jsonl

Following are descriptions of each fields in the data

* ``year`` - year of outbreak
* ``week`` - the `epidemiological week <http://www.cmmcp.org/epiweek.htm>`_ of
  outbreak
* ``locality`` - location of outbreak
* ``district_zone_pbt`` - district/zone/pbt of location
* ``state`` - state which the location belong in
* ``length_of_outbreak_days`` - length of outbreak
* ``total_accumulated_cases`` - total cases in data point

    
Creating A Simple Dashboard
============================

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
--------------------------------------

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
``src/example/dengueviz/routes.zcml`` and add these lines:

.. code-block:: xml

   <route name="example.dengueviz.json"
         pattern="/example.dengueviz.json"/>

Looking at the data, we can see that we need to convert the epiweeks to
datetime for visualizing as a time series data. There is a python module for
this in github, let download it into our project.

.. code-block:: bash

   wget https://gist.githubusercontent.com/kagesenshi/2c53e855e776472723f4/raw/59ce71b7c6dbc027a5abfa4d9cba68bb9d58b801/epiweek.py \
        -O src/example/dengueviz/epiweek.py

Edit ``src/example/dengueviz/view.py`` and add these lines:

* at the top of the file:

.. code-block:: python

   import epiweek

* in the ``Views`` class.

.. code-block:: python

   @view_config(route_name='example.dengueviz.json',
                renderer='json')
   def json_view(self):
       # load data into memory
       f = asset.load('example.dengueviz:dengue-hotspot.jsonl')
       data = [json.loads(l) for l in f]
    
       # select only fields we want
       data = [{'epiweek': d['week'],
                'date': epiweek.first_day(d['week'],
                                d['year']).strftime('%Y-%m-%d'),
                'year': d['year'],
                'state': d['state'].upper(),
                'count': d['total_accumulated_cases']} for d in data]

       # publish
       return data

Start the server and using your browser, load
http://localhost:6543/example.dengueviz.json

You should be getting a JSON output. We will use this JSON output for the
dashboard.

.. seealso::
   
   `Pyramid Route Pattern Syntax <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html#route-pattern-syntax>`_
        URL Route patterns documentation.

   `Pyramid View <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/views.html>`_
        Pyramid Views documentations. Please take note that Pysiphae uses
        views that are attached to classes.
   
   `Asset <https://pypi.python.org/pypi/asset/>`_
        Asset library documentation.




Create Dashboard View
----------------------

In ``src/example/dengueviz/view.py``, you will see that there is already one
view under the name as ``default_view``. The view's template is in
``src/example/dengueviz/templates/default.pt``.

We want to develop a simple dashboard with 2 chart elements, a line chart 
showing case count, and a row chart showing states.

Clear the contents of ``default.pt`` and replace with this:

.. code-block:: xml

   <metal:master use-macro="view.main_template">
       <metal:style fill-slot="style_slot">
           // put CSS here
       </metal:style>
       <metal:header fill-slot="header">
           <h1>Dengue Visualization</h1>
       </metal:header> 
       <metal:content fill-slot="content">
            <div class="row">
                <div class="col-lg-8 col-sm-8">
                    <div class="panel panel-default">
                        <div class="panel-header">
                            Cases Over Time
                        </div>
                        <div class="panel-body">
                            <div id="casetime-chart"></div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-sm-4">
                    <div class="panel panel-default">
                        <div class="panel-header">
                            States
                        </div>
                        <div class="panel-body">
                            <div id="state-chart"></div>
                        </div>
                    </div>
                </div>
            </div>    
       </metal:content>
       <metal:script fill-slot="javascript_footer_slot">
            <script src="/++static++example.dengueviz/default.js"></script>
       </metal:script>
   <metal:master>

Following is a description of the template above:

* Create a layout for dashboard elements:

  * ``#casetime-chart`` - placeholder for case over time chart
  * ``#state-chart`` - placeholder for state row chart

* Include javascript for rendering charts

Now let create javascript code for rendering the charts:

.. code-block:: javascript

   var caseTimeChart = dc.lineChart('#casetime-chart');
   var stateChart = dc.rowChart('#state-chart');

   d3.json('/example.dengueviz.json', function (data) {
       var ndx = crossfilter(data);
       var timeDim = ndx.dimension(function (d) { 
            return new Date(d.date);
       });
       var timeCount = timeDim.group().reduceSum(function (d) { 
            return d.count;
       });

       caseTimeChart.options({
            height: 500,
            width: 700,
            dimension: timeDim,
            group: timeCount,
            x: d3.time.scale(),
            elasticX: true
       });

       caseTimeChart.render();

       var stateDim = ndx.dimension(function (d) { return d.state });
       var stateCount = stateDim.group().reduceSum(function (d) {
            return d.count;
       });

       stateChart.options({
            height: 500,
            width: 300,
            dimension: stateDim,
            group: stateCount,
            elasticX: true
       });

       stateChart.render();
   });

Start the server, and load http://localhost:6543/example.dengueviz. The
visualization should appear on that page.

.. seealso::

   `Bootstrap Grid System <http://getbootstrap.com/css/#grid>`_
        Grid system for layout

   `DC.js <http://dc-js.github.io/dc.js/>`_
        Dimensional Charting Javascript library used for visualization

   `DC.js Examples <http://dc-js.github.io/dc.js/examples/>`_
        Example implementation of DC.js charts

   `D3.js <http://d3js.org>`_
        Data Driven Document visualization library

   `dc-addons <https://github.com/Intellipharm/dc-addons>`_
        Additional charts for DC.js

Registering navigation elements
===============================

Setting dashboard as home view
===============================

