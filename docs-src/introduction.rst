Introduction to Pysiphae
========================

Pysiphae is a framework for developing dashboards. It takes care of
all the nitty-gritty content management stuff and let data engineers focus in
doing what they do best - preparing and visualizing data.

Features of Pysiphae framework includes:

* Pre-integrated Javascript libraries

  * `d3.js <http://www.d3.js>`_
  * `dc.js <https://dc-js.github.io/dc.js>`_
  * `dc-addons.js <https://github.com/Intellipharm/dc-addons>`_
  * `leaflet.js <http://leafletjs.com>`_
  * dc-heatmap.js
  * `heatmap.js <http://www.patrick-wied.at/static/heatmapjs>`_
  * `jsplumb <https://jsplumbtoolkit.com/>`_
  * `dimple.js <http://dimplejs.org>`_
  * `MathJax <http://mathjax.org>`_

* Pre-integrated Python libraries

  * `Pyramid <http://www.pylonsproject.org/>`_
  * `zope.component <http://muthukadan.net/docs/zca.html/>`_
  * `SQLAlchemy <http://www.sqlalchemy.org/>`_
  * `Elasticsearch DSL <http://elasticsearch-dsl.readthedocs.org/>`_
  * `ZODB3 <http://www.zodb.org/>`_
  * `python-memcached <https://pypi.python.org/pypi/python-memcached>`_
  * `HappyBase <https://happybase.readthedocs.org/>`_
  * `PyYAML <http://pyyaml.org/>`_

* Simplified API for developing views for data visualization
* Basic theme based off AdminLTE theme
* Authentication/Authorization engine based on `repoze.who
  <https://repozewho.readthedocs.org/>`_:

  * htpasswd user db
  * LDAP user db
  * configuration driven permission assignment

* Memoize caching using `wraptor <https://pypi.python.org/pypi/Wraptor>`_

Architecture
------------

.. graphviz::

   graph Arch {
    compound=true;
    graph [splines=ortho];
    node [shape=component];

    subgraph cluster_tools {
        node [shape=box];
        templer [label="pysiphae.templer\n(Code Generator)"];
        buildout [label="buildout\n(Environment\nBuilder)"];
        ansible [label="ansible\n(Deployment Tool)"];
        bower [label="bower\n(Javascript\nPkgMgr)"];
        label="CLI Tools"
    }

    subgraph cluster_registries {
        viewplugin [label="View Plugin", shape=box3d];
        authplugin [label="Authentication Plugin", shape=box3d];
        storageplugin [label="Storage Plugin", shape=box3d];
        payloadplugin [label="Payload Plugin", shape=box3d];
        viewplugin -- authplugin [style=invis];
        authplugin -- storageplugin [style=invis];
        storageplugin -- payloadplugin [style=invis];
        color="#000000";
        label="Registries";
    }

    subgraph cluster_proxy {
        proxy [label="node-http-proxy\n(Routing Proxy)"];
        color="black";
        label="Proxy Service";
    }
    subgraph cluster_processmgr {
        procmgr [label="pysiphae.processmgr\n(Process Manager)"];   
        color="black";
        label="Process Execution\nService";
    }
    subgraph cluster_web {
        { rank=same;
            wsgi [label="pysiphae.wsgi\n(Web Application)"];
        }
        { rank=same;
            views [label="pysiphae.views\n(Core Views)"];
            runner [label="pysiphae.runner\n(Process Runner)"];
        }
        pyramid [shape=folder,label="Pyramid\n(Base Framework)"];
        auth [label="repoze.who\n(Authorization)"];
        registry [label="zope.components\n(Component Registry)"];
        storages [label="pysiphae.storages\n(Storage Factories)"];
        color="black";
        label="Web Application\nService";
    }

    browser [shape=ellipse, label="Web Browser"];
    buildout -- browser [ltail=cluster_tools, style=invis];
    browser -- proxy [lhead=cluster_proxy];
    proxy -- wsgi;
    proxy -- procmgr;
    wsgi -- auth;
    auth -- views;
    wsgi -- views;
    runner -- views;
    views -- pyramid;
    runner -- pyramid;
    views -- storages;
    procmgr -- runner;
    registry -- pyramid;
    storages -- pyramid;
    authplugin -- registry [ltail=cluster_registries];
   }
