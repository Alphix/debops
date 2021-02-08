.. Copyright (C) 2022 David Härdeman <david@hardeman.nu>
.. Copyright (C) 2022 DebOps <https://debops.org/>
.. SPDX-License-Identifier: GPL-3.0-only

Description
===========

Kerberos is a network authentication protocol that works on the basis of one or
more servers (`Key Distribution Centers` or `KDCs`) which act as a trusted
third party. The KDCs issue `tickets` to services and users which allows for
mutual authentication (i.e. the user is authenticated to the server and vice
versa).

The ``debops.kerberos`` Ansible role can be used to configure the `Kerberos`__
environment on one or more hosts by creating principals and managing the
:file:`/etc/krb5.conf` configuration file.

.. __: https://web.mit.edu/kerberos/

The Kerberos support in DebOps is tightly integrated with, and depends upon, a
working LDAP configuration (see the :ref:`debops.ldap` and :ref:`debops.slapd`
roles).

After LDAP has been properly setup and configured, and one or more Kerberos
server(s) (see :ref:`debops.kerberos_server`) have been configured, this role
can be used to set up the system-wide Kerberos configuration on a Debian/Ubuntu
host, and provide Kerberos-based applications, as well as other Ansible roles,
(such as :ref:`debops.sssd` and :ref:`debops.nfs`), with the information
necessary to make use of Kerberos.

In addition to that, this role can be used via the Ansible inventory, or as
a dependent role by other Ansible roles, to perform various Kerberos-related
tasks (creation of Kerberos principals, keytabs, policies, etc) by itself, on
behalf of the Ansible user.
