.. Copyright (C) 2017      Robin Schneider <ypid@riseup.net>
.. Copyright (C) 2019      Maciej Delmanowski <drybjed@gmail.com>
.. Copyright (C) 2017-2019 DebOps <https://debops.org/>
.. SPDX-License-Identifier: GPL-3.0-only

.. _neurodebian__ref_getting_started:

Getting started
===============

.. only:: html

   .. contents::
      :local:


Example inventory
-----------------

To install packages from NeuroDebian on a given host or set of hosts, they need
to be added to the ``[debops_service_neurodebian]`` Ansible group in the
inventory:

.. code:: ini

   [debops_service_neurodebian]
   hostname


Example playbook
----------------

If you are using this role without DebOps, here's an example Ansible playbook
that uses the ``debops.neurodebian`` role:

.. literalinclude:: ../../../../ansible/playbooks/service/neurodebian.yml
   :language: yaml
   :lines: 1,6-


Ansible tags
------------

You can use Ansible ``--tags`` or ``--skip-tags`` parameters to limit what
tasks are performed during Ansible run. This can be used after a host was first
configured to speed up playbook execution, when you are sure that most of the
configuration is already in the desired state.

Available role tags:

``role::neurodebian``
  Main role tag, should be used in the playbook to execute all of the role
  tasks as well as role dependencies.

``role::neurodebian:package``
  Tasks related to system package management like installing or
  removing packages.
