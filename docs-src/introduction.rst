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

Project Sponsors
-----------------

- `Abyres Enterprise Technologies Sdn Bhd <http://www.abyres.net>`_

Contributors
-------------

- Izhar Firdaus <izhar@kagesenshi.org>
