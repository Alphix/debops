.. Copyright (C) 2022 David Härdeman <david@hardeman.nu>
.. Copyright (C) 2022 DebOps <https://debops.org/>
.. SPDX-License-Identifier: GPL-3.0-only

Getting started
===============

.. only:: html

   .. contents::
      :local:


Example inventory
-----------------

To enable the Kerberos server(s) on a host, you need to add it to the
``[debops_service_kerberos_server]`` (for a single standalone server),
``[debops_service_kerberos_server_primary]`` (for the master server, in case
there are more than one Kerberos server), or
``[debops_service_kerberos_server_secondary]`` Ansible inventory group. At
least one host should already have been configured with the :ref:`debops.slapd`
role (see its documentation for more details).

The recommended setup is to make the same host which is running the
:command:`slapd` server the `primary` Kerberos server:

.. code-block:: none

   [debops_service_slapd]
   hostname

   [debops_service_kerberos_server_primary]
   hostname

   [debops_service_kerberos_server_secondary]
   someotherhostname


See also the (FIXME - ref - ``debops.kerberos``) role for hosts which should be integrated
in, and make use of, the Kerberos environment.


Example playbook
----------------

If you are using this role without DebOps, here's an example Ansible playbook
that uses the ``debops.kerberos_server`` role:

.. literalinclude:: ../../../../ansible/playbooks/service/kerberos_server.yml
   :language: yaml
   :lines: 1,5-


Ansible tags
------------

You can use Ansible ``--tags`` or ``--skip-tags`` parameters to limit what
tasks are performed during Ansible run. This can be used after host is first
configured to speed up playbook execution, when you are sure that most of the
configuration has not been changed.

Available role tags:

``role::kerberos_server``
  Main role tag, should be used in the playbook to execute all of the role
  tasks as well as role dependencies.

``role::kerberos_server:config``
  Controls whether tasks related to the creation of configuration files should
  be executed.

``role::kerberos_server:packages``
  Controls whether tasks related to the installation of Kerberos packages
  should be executed.

``role::kerberos_server:realms``
  Controls whether tasks related to the creation/configuration of Kerberos
  realms should be executed.

``role::kerberos_server:realms:create``
  Controls whether tasks related to the creation of Kerberos realms should be
  executed.

``role::kerberos_server:realms:config``
  Controls whether tasks related to the configuration of Kerberos realms should
  be executed.

``role::kerberos_server:realms:ldap``
  Controls whether tasks related to the LDAP configuration of Kerberos realms
  should be executed.


Other resources
---------------

List of other useful resources related to the ``debops.kerberos_server``
Ansible role:

- Manual pages: :man:`kadmind(8)`, :man:`kadmin(8)`, :man:`kadmin(1)`,
  :man:`kerberos(1)`, :man:`krb5kdc(8)` and :man:`krb5.conf(5)`.

- The website of the `MIT Kerberos Project`__, in particular the
  `documentation for administrators`__.

  .. __: https://web.mit.edu/kerberos/
  .. __: https://web.mit.edu/kerberos/krb5-latest/doc/admin/index.html
