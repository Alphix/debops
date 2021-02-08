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

The ``debops.kerberos_server`` Ansible role can be used to configure the
:command:`kadmind` and :command:`krb5kdc` daemons (part of the `MIT Kerberos`__
project) on one or more servers and to integrate various hosts in the Kerberos
environment. The role automatically integrates the Kerberos environment with
the LDAP environment setup by the :ref:`debops.ldap` and :ref:`debops.slapd`
roles and stores all Kerberos data in the LDAP DIT.

.. __: https://web.mit.edu/kerberos/
