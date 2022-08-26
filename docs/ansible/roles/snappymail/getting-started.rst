.. Copyright (C) 2022 David Härdeman <david@hardeman.nu>
.. Copyright (C) 2022 DebOps <https://debops.org/>
.. SPDX-License-Identifier: GPL-3.0-only

.. _snappymail__ref_getting_started:

Getting started
===============

.. include:: ../../../includes/global.rst

.. only:: html

   .. contents::
      :local:

.. _snappymail__ref_default_setup:

Default setup
-------------

If you don't specify any configuration values, the role will use
:ref:`debops.nginx` to setup a HTTP server running an installation of
a recent `SnappyMail`__ release which is made available via
``https://webmail.<your-domain>``. By default, SQLite will be used to
store per-user settings and address books (see :envvar:`snappymail__database`
and :envvar:`snappymail__database_map` for other options).

When the :ref:`LDAP infrastructure <debops.ldap>` is detected on the SnappyMail
host, the role will install and configure LDAP plugins in SnappyMail.
These plugins enable contact lookups in the LDAP directory and allow users
to change their own password.

SnappyMail will use the current user credentials to login to the LDAP
directory, therefore access to the LDAP entries and attributes depends on the
LDAP ACL configuration in the directory itself.

.. __: https://snappymail.eu/


.. _snappymail__ref_srv_records:

IMAP, SMTP and Sieve server detection
-------------------------------------

First of all, this role detects the presence of the :ref:`debops.imapproxy`
role using Ansible local facts on the host. If it is found, it will be used
to connect to the IMAP server.

Next, the role detects the preferred IMAP, SMTP and Sieve servers by using
:ref:`dns_configuration_srv` for the following services:

.. code-block:: none

   _imap._tcp.{{ snappymail__domain }} (default port 143)
   _imaps._tcp.{{ snappymail__domain }} (default port 993)
   _submissions._tcp.{{ snappymail__domain }} (default port 465)
   _sieve._tcp.{{ snappymail__domain }} (default port 4190)

At the moment, only a single SRV resource record is supported for each service.

If the above SRV resource records are not available, the role will check for
the presence of the :ref:`debops.dovecot` and :ref:`debops.postfix` roles using
Ansible local facts on the host. If they are found, the respective service
(IMAP, SMTP and/or Sieve) will be configured to be accessed via the host's own
FQDN address to support X.509 certificate verification.

Finally, the role will fall back to using static domain names for the
respective services, based on the host domain (:envvar:`snappymail__domain`):

.. code-block:: none

   IMAP:  imap.example.org:993
   SMTP:  smtp.example.org:465
   Sieve: sieve.example.org:4190

This allows for deployment of SnappyMail independently from the respective
services, for example on a separate host or using a VM. The communication with
the mail services will be encrypted by default using Implicit TLS, as
recommended by :rfc:`8314`.


.. _snappymail__ref_example_inventory:

Example inventory
-----------------

To install and configure SnappyMail on a host, it needs to be present in the
``[debops_service_snappymail]`` Ansible inventory group. Additional services
like: :ref:`Redis <debops.redis_server>`, or
:ref:`memcached <debops.memcached>`;
:ref:`PostgreSQL <debops.postgresql_server>` or
:ref:`MariaDB <debops.mariadb_server>`; and
:ref:`imapproxy <debops.imapproxy>`
can help increase the website performance.

.. code-block:: none

   [debops_all_hosts]
   webmail

   [debops_service_postgresql_server]
   webmail

   [debops_service_redis_server]
   webmail

   [debops_service_imapproxy]
   webmail

   [debops_service_snappymail]
   webmail


.. _snappymail__ref_example_playbook:

Example playbook
----------------

The following playbook can be used with DebOps. If you are using this role
without DebOps you might need to adapt it to make it work in your setup.

.. literalinclude:: ../../../../ansible/playbooks/service/snappymail.yml
   :language: yaml
   :lines: 1,5-

This playbook is also shipped with DebOps at
:file:`ansible/playbooks/service/snappymail.yml`.


.. _snappymail__ref_ansible_tags:

Ansible tags
------------

You can use Ansible ``--tags`` or ``--skip-tags`` parameters to limit what
tasks are performed during Ansible run. This can be used after a host was first
configured to speed up playbook execution, when you are sure that most of the
configuration is already in the desired state.

Available role tags:

``role::snappymail``
  Main role tag, should be used in the playbook to execute all of the role
  tasks as well as role dependencies.

``role::snappymail:pkg``
  Run tasks related to system package installation.

``role::snappymail:deployment``
  Run tasks related to the application deployment and updates.

``role::snappymail:config``
  Run tasks related to the application configuration.

``role::snappymail:plugins``
  Run tasks related to plugin deployment, configuration and updates.

``role::snappymail:database``
  Run tasks related to seting up the database user and schema.

``role::snappymail:backup``
  Run tasks related to seting up backup scripts.
