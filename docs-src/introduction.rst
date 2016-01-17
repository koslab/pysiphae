Introduction to Pysiphae
========================

Pysiphae is a framework for developing dashboards. It takes care of
all the nitty-gritty content management stuff and let data engineers focus in
doing what they do best - preparing and visualizing data.

Source code is available at https://github.com/koslab/pysiphae.

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

Why Pysiphae?
--------------

Pysiphae is designed to solve the following problems when building an
enterprise application for data visualization:

* Reduce the effort of reimplementing common functionalities of an enterprise
  web application through:

  * Using pluggable authentication system that supports common enterprise
    authentication backend such as LDAP.
  * Implements default style and templates for common functionalities such as
    login screen, navigation, main template.
  * Pluggable storage system that allow implementation of custom components for
    storing/querying data
  * Pluggable viewlet/viewgroup system that allow implementing snippets that
    can be inserted into main templates without modifying the main template
    itself
  * Pluggable payload execution system for executing ETL scripts
  * Kerberos integration for Hadoop security compatibility (TBD)
  * Configuration driven ACL, component registries

The design of Pysiphae as a framework is heavily influenced by Plone as the
author was primarily a Plone developer before switching to a different role.
Pysiphae implements many Plone patterns that the author consider really useful
for his development needs.

Pysiphae utilizes Zope Component Architecture for many of its functionalities
but exposes API that minimizes the need for devs to touch the component engines
itself

Wishlist
---------

A listing of features that would be great for future versions:

* Vega-like configuration language implementation for defining data
  visualization dashboard
* Data collection endpoints for collecting common statistics
* Repository of reusable plugins/components
* Theme engine ala plone.app.theming

Project Sponsors
-----------------

- `Abyres Enterprise Technologies Sdn Bhd <http://www.abyres.net>`_

Contributors
-------------

- Izhar Firdaus <izhar@kagesenshi.org>

Credit
------

- This framework was originally built as a platform for development of
  data visualization applications for a project for 
  `Malaysian Administrative Modernization and Management Unit 
  (MAMPU) <http://www.mampu.gov.my>`_
