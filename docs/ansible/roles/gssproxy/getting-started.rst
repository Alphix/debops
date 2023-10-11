.. Copyright (C) 2023 David Härdeman <david@hardeman.nu>
.. Copyright (C) 2023 DebOps <https://debops.org/>
.. SPDX-License-Identifier: GPL-3.0-only

Getting started
===============

.. only:: html

   .. contents::
      :local:


Introduction
------------

By default, the role will install the daemon, including a very basic
configuration. To actually make use of :command:`gssproxy`, you also need to
configure application-specific configuration files using the
``gssproxy__*_configuration`` variables (see :ref:`gssproxy__ref_configuration`
for details).


Example inventory
-----------------

To manage the :command:`gssproxy` service, the host needs to be included in the
``[debops_service_gssproxy]`` Ansible inventory group:

.. code-block:: none

   [debops_all_hosts]
   hostname

   [debops_service_gssproxy]
   hostname


Example playbook
----------------

If you are using this role without DebOps, here's an example Ansible playbook
that uses the ``debops.gssproxy`` role:

.. literalinclude:: ../../../../ansible/playbooks/service/gssproxy.yml
   :language: yaml
   :lines: 1,5-


Ansible tags
------------

You can use Ansible ``--tags`` or ``--skip-tags`` parameters to limit what
tasks are performed during Ansible run. This can be used after a host was first
configured to speed up playbook execution, when you are sure that most of the
configuration is already in the desired state.

Available role tags:

``role::gssproxy``
  Main role tag, should be used in the playbook to execute all of the role
  tasks as well as role dependencies.
