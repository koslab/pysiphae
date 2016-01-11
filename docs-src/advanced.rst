===============
Advanced Topic
===============

Caching data
=============

Currently caching can be implemented using Wraptor. A more comprehensive
caching will be developed later with multiple backends:

Refer: https://pypi.python.org/pypi/Wraptor

Template Variables
=====================

By default, pysiphae includes the following variables on the ``view`` object in
page templates:

* ``view.main_template`` - main template macros object
* ``view.request`` - request object
* ``view.vars`` - pluggable template variable holder. Also available as
  ``vars``

Using spinners
===============

A helper javascript function is included for displaying spinner.

.. code-block:: javascript

   pysiphae.startSpinner();

   d3.json(url, function (data) {
       // do something
       pysiphae.stopSpinner();
   });

Authentication
===============

HTPasswd
--------

In ``development.ini`` there is a sample configuration that enables
htpasswd authentication. Uncomment them to enable.

.. code-block:: ini

   [app:pysiphae]

   # set default permission for views with undefined permission
   pysiphae.default_permission = pysiphae.View

   # grant ACL to group
   pysiphae.acl =
      Allow,group:LoggedIn,pysiphae.View

   # assign groups to user
   pysiphae.roles =
      username=group:groupname0,group:groupname1
   
To add a user into htpasswd, use the following command:

.. code-block:: bash

   htpasswd -d htpasswd <username>

LDAP
----

LDAP Authentication can be enabled by using this 
``who.ini``:

.. code-block:: ini
   
   [plugin:redirector]
   # identificaion and challenge
   use = repoze.who.plugins.redirector:make_plugin
   login_url = /login
   
   [plugin:auth_tkt]
   # identification and authentication
   use = repoze.who.plugins.auth_tkt:make_plugin
   secret = s33kr1t
   cookie_name = oatmeal
   secure = False
   include_ip = False
   
   [plugin:ldap]
   # authentication
   use = repoze.who.plugins.ldap:LDAPAuthenticatorPlugin
   ldap_connection = ldap://<server>:<port>/
   base_dn = <base-dn>
   
   [plugin:ldapattr]
   use = pysiphae.who:make_ldapattr_plugin
   url = ldap://<server>:<port>/
   attributes = memberOf,title,ou,givenName,mail
   bind_dn = <bind-dn>
   bind_password = <password>
   
   [general]
   request_classifier = repoze.who.classifiers:default_request_classifier
   challenge_decider = repoze.who.classifiers:default_challenge_decider
   remote_user_key = REMOTE_USER
   
   [identifiers]
   # plugin_name;classifier_name:.. or just plugin_name (good for any)
   plugins =
         auth_tkt
   
   [authenticators]
   # plugin_name;classifier_name.. or just plugin_name (good for any)
   plugins =
         auth_tkt
         ldap
   
   [challengers]
   # plugin_name;classifier_name:.. or just plugin_name (good for any)
   plugins =
         redirector;browser
   
   [mdproviders]
   plugins =
       ldapattr
   

Authorization
==============

Authorization in Pysiphae utilizes the core authorization engine by Pyramid. 

Refer: http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/security.html#protecting-views-with-permissions
