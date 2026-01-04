.. Copyright (C) 2022 David Härdeman <david@hardeman.nu>
.. Copyright (C) 2022 DebOps <https://debops.org/>
.. SPDX-License-Identifier: GPL-3.0-only

.. _snappymail__ref_ldap_dit:

LDAP Directory Information Tree
===============================

This document describes how the :ref:`debops.snappymail` Ansible role fits in
the :ref:`ldap__ref_dit`.


Directory structure
-------------------

- :ref:`cn=host.example.org <ldap__ref_ldap_dit>` -> :ref:`debops.ldap`

  - :envvar:`uid=snappymail <snappymail__ldap_self_rdn>`


Object Classes and Attributes
-----------------------------

- :envvar:`uid=snappymail <snappymail__ldap_self_rdn>`

  - :ref:`debops.snappymail`: :envvar:`Object Classes <snappymail__ldap_self_object_classes>`, :envvar:`Attributes <snappymail__ldap_self_attributes>`


Parent nodes
------------

- :ref:`debops.ldap <ldap__ref_ldap_dit>`

  - :envvar:`ansible_local.ldap.base_dn <ldap__base_dn>` -> :envvar:`snappymail__ldap_base_dn`

  - :envvar:`ansible_local.ldap.device_dn <ldap__device_dn>` -> :envvar:`snappymail__ldap_device_dn`


Child nodes
-----------

There are no child nodes defined for the :ref:`debops.snappymail` Ansible role.
