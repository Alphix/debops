.. Copyright (C) 2022 David Härdeman <david@hardeman.nu>
.. Copyright (C) 2022 DebOps <https://debops.org/>
.. SPDX-License-Identifier: GPL-3.0-only

Getting started
===============

.. only:: html

   .. contents::
      :local:

.. include:: ../../../includes/global.rst


Ansible Controller requirements
-------------------------------

If you plan to use this role to perform Kerberos tasks in the default
configuration, you need to install the ``krb5-user`` package on the Controller
host.


.. _kerberos__ref_admin:

Kerberos administrator initialization
-------------------------------------

The basic setup of the Kerberos realm(s) is defined and managed by the
:ref:`debops.kerberos_server` Ansible role. The
:envvar:`kerberos_server__combined_realms` variable contains a list of the
Kerberos realms and their related policies, LDAP entries, etc which will be
created on server installation (see :envvar:`kerberos_server__default_realms`
for the default realm).

The :file:`ansible/playbooks/kerberos/init-kerberos-admin.yml` Ansible playbook
can be used to create a Kerberos principal for an existing admin account in the
LDAP directory (see :ref:`ldap__ref_ldap_init`). To use it with a new
installation, first make sure you have a working LDAP environment and that at
least the primary Kerberos server has been setup, then run the command:

.. code-block:: console

   debops run kerbero/init-kerberos-admin -l <primary-kerberos-server>

The playbook will use the current UNIX account information on the Ansible
Controller and the LDAP configuration information stored on the primary
Kerberos server to determine the distinguished name of the administrator
account in the LDAP directory.

It will then create a new kerberos principal by connecting directly to the
primary Kerberos server and running :man:`kadmin.local(8)`. This principal will
be stored under the ``cn=<realm>,cn=Kerberos,ou=Services,dc=example,dc=org``
subtree and linked to the administrator account in the LDAP tree. If we assume
that the admin account is ``uid=foobar,ou=People,dc=example,dc=org``, then the
new principal will be named ``foobar/admin@EXAMPLE.ORG``, stored in the LDAP
directory under
``krbPrincipalName=foobar/admin@EXAMPLE.ORG,cn=EXAMPLE.ORG,cn=Kerberos,ou=Services,dc=example,dc=org``,
and the admin account will automatically be updated so that the
``krbPrincipalReferences`` attribute (which is multi-valued) includes a
back-reference to the principal.

This principal has two uses: it can be used to authenticate to the LDAP server
as ``uid=foobar,ou=People,dc=example,dc=org``, and it can also be used with the
:man:`kadmin(8)` tool to perform administrative tasks in the Kerberos database.

By default, the playbook will also store a copy of the principal in a keytab on
the Ansible Controller (by default, under :file:`secret/kerberos/admin.keytab`)
together with a basic :file:`krb5.conf` file (to provide some reasonable
defaults in case the Ansible Controller host is not managed with DebOps and/or
lacks a central :file:`/etc/krb5.conf` file). These two files, in combination,
allows administrative commands to be performed without further user input.

.. warning:: The administrator keytab is not protected by a password or anything
             similar, and provides unrestricted access to the LDAP directory
             and to the administrative interface of the Kerberos infrastructure.
             It therefore needs to be protected (e.g. by encrypting the
             :file:`secret/` directory, see :ref:`debops.secret`) in the same
             manner that you'd protect a root password.


Example inventory
-----------------

The :ref:`debops.kerberos` role is included in the DebOps common playbook,
therefore you don't need to do anything special to enable it on a host. However
it is deactivated by default.

To enable the role, define in the Ansible inventory, for example in the
:file:`ansible/inventory/group_vars/all/kerberos.yml` file:

.. code-block:: yaml

   kerberos__enabled: True

The :ref:`debops.kerberos` role is used by other DebOps roles, and enabling it
will affect the environment and configuration of multiple services (e.g.
:ref:`debops.sssd` and :ref:`debops.nfs`), therefore you might want to
enable Kerberos support at the beginning of a new deployment.


Example playbook
----------------

If you are using this role without DebOps, here's an example Ansible playbook
that uses the ``debops.kerberos`` role:

.. literalinclude:: ../../../../ansible/playbooks/service/kerberos.yml
   :language: yaml
   :lines: 1,5-


Ansible tags
------------

You can use Ansible ``--tags`` or ``--skip-tags`` parameters to limit what
tasks are performed during Ansible run. This can be used after host is first
configured to speed up playbook execution, when you are sure that most of the
configuration has not been changed.

Available role tags:

``role::ldap``
  Main role tag, should be used in the playbook to execute all of the role
  tasks as well as role dependencies.

``role::ldap:tasks``
  Run the LDAP tasks generated by the role in the LDAP directory.


Other resources
---------------

List of other useful resources related to the ``debops.kerberos`` Ansible role:

Manual pages:

- :man:`kadmin(1)`
- :man:`kinit(1)`
- :man:`klist(1)`
- :man:`kdestroy(1)`
- :man:`kpasswd(1)`
- :man:`ktutil(1)`
- :man:`krb5.conf(5)`

The website of the `MIT Kerberos Project`__, in particular the documentation:

.. __: https://web.mit.edu/kerberos/

- `for users`__

  .. __: https://web.mit.edu/kerberos/krb5-latest/doc/user/index.html

- `for administrators`__

  .. __: https://web.mit.edu/kerberos/krb5-latest/doc/admin/index.html
