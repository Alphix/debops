.. Copyright (C) 2023 David Härdeman <david@hardeman.nu>
.. Copyright (C) 2023 DebOps <https://debops.org/>
.. SPDX-License-Identifier: GPL-3.0-only

Kerberos
========

.. only:: html

   .. contents::
      :local:


Introduction
------------

The Kerberos integration in DebOps is still not complete, you need to first
manually setup a working Kerberos environment, including KDCs and
:file:`/etc/krb5.conf` on your servers and hosts. This will be further
improved in the future.


LDAP
----

If you want to use Kerberized NFS, you are strongly encouraged to also make
sure that you have LDAP configured on all servers and clients (refer to the
:ref:`debops.slapd` and :ref:`debops.ldap` roles for information on how to
setup LDAP).


Principal
---------

Next, a Kerberos principal needs to be created for each server. The principal
needs to have the form ``nfs/<server_fqdn>@REALM`` (e.g.
``nfs/server.example.com@EXAMPLE.COM``). This principal needs to be exported
to a keytab and stored in :file:`/etc/krb5.keytab.d/nfs.keytab`:

.. code-block:: console

   mkdir /etc/krb5.keytab.d
   kadmin
   kadmin: add_principal -randkey -policy randkey nfs/server.example.com
   Principal "nfs/server.example.com/EXAMPLE.COM" created.
   kadmin: ktadd -k /etc/krb5.keytab.d/nfs.keytab nfs/server.example.com
   kadmin: Entry for principal nfs/server.example.com@EXAMPLE.COM with
             kvno 2, encryption type AES256-CTS-HMAC-SHA96 added to keytab
             WRFILE:/etc/krb5.keytab.d/nfs.keytab.
   kadmin: quit


Inventory
---------

Finally, you need to make sure that :envvar:`nfs_server__kerberos`,
:envvar:`nfs_server__kerberos_princ`, :envvar:`nfs_server__kerberos_realms`
and :envvar:`nfs_server__domain` are configured in your Ansible inentory:

.. code-block:: yaml

   nfs_server__kerberos: True

   nfs_server__kerberos_princ: 'nfs/server.example.com@EXAMPLE.COM'

   nfs_server__kerberos_realms: [ 'EXAMPLE.COM' ]

   nfs_server__domain: 'example.com'
