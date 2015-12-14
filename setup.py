import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_zcml',
    'zope.component',
    'waitress',
    'SQLAlchemy',
    'pyhive',
    'python-memcached',
    'happybase',
    'elasticsearch',
    'elasticsearch_dsl',
    'ZODB3',
    'Paste',
    'pymongo',
    'wraptor',
    'sasl',
    'thrift',
    'thrift_sasl',
    'templer.core'
]

setup(name='pysiphae',
      version='0.0',
      description='pysiphae',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="pysiphae",
      entry_points="""\
      [paste.app_factory]
      main = pysiphae:main

      [paste.paster_create_template]
      pysiphae_dashplugin = pysiphae.templer:DashPlugin
      """,
      )
