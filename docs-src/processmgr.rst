================
Process Manager
================

Pysiphae also includes a process manager daemon for execution of processes in
command line. The process manager daemon was developed to manage the execution
of command line scripts (Sqoop, Spark, HiveQL) on Hadoop client node.

A process manager UI is included in Pysiphae dashboard for executing the jobs

.. warning::

   The process management server does not have authentication. ONLY run it in a
   secure environment.

Registering Process Payload
============================

.. code-block:: python

   from pysiphae.processmgr.payload import factory

   p1 = factory(
       name='uname payload',
       description='Get uname of the process management server',
       executor='shell',
       files=None,
       options=None
   )

Parameters:

* ``name`` - name of payload

* ``description`` - short description of payload

* ``executor`` - executor to use from the server side

* ``files`` - asset spefication pointing to files to upload to server

* ``options`` - additional options to pass to executor
