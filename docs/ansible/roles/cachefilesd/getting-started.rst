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
configuration (at :file:`/etc/cachefilesd.conf`). To actually make use of
:command:`cachefilesd`, you also need to make sure that the the filesystem that
is used to store data (by default, under :file:`/var/cache/fscache/` is mounted
with extended user attribute support (``user_xattr``) enabled. Furthermore,
when mounting the remote filesystem, an extra option typically needs to be
included to instruct the kernel to use the cache.

For example, if your :file:`/etc/fstab` includes these lines (this is assuming
that no separate mount point for :file:`/var` is defined):

.. code-block:: none

   /dev/sda3                   /     ext4  <options>
   ...
   nfsserver.example.com:/srv  /srv  nfs4  <options>

They would have to be amended to instead read:

.. code-block:: none

   /dev/sda3                   /     ext4  <options>,user_xattr
   ...
   nfsserver.example.com:/srv  /srv  nfs4  <options>,fsc

Note that using :command:`cachefilesd` to cache network filesystem data is not
guaranteed to offer performance benefits. The local caching can speed up
read-mostly workloads and reduce network bandwidth usage, but has the potential
to slow down write-intensive workloads.


Example inventory
-----------------

To manage the :command:`cachefilesd` service, the host needs to be included in
the ``[debops_service_cachefilesd]`` Ansible inventory group:

.. code-block:: none

   [debops_all_hosts]
   hostname

   [debops_service_cachefilesd]
   hostname


Example playbook
----------------

If you are using this role without DebOps, here's an example Ansible playbook
that uses the ``debops.cachefilesd`` role:

.. literalinclude:: ../../../../ansible/playbooks/service/cachefilesd.yml
   :language: yaml
   :lines: 1,5-


Ansible tags
------------

You can use Ansible ``--tags`` or ``--skip-tags`` parameters to limit what
tasks are performed during Ansible run. This can be used after a host was first
configured to speed up playbook execution, when you are sure that most of the
configuration is already in the desired state.

Available role tags:

``role::cachefilesd``
  Main role tag, should be used in the playbook to execute all of the role
  tasks as well as role dependencies.
