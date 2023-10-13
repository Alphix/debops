.. Copyright (C) 2023 David Härdeman <david@hardeman.nu>
.. Copyright (C) 2023 DebOps <https://debops.org/>
.. SPDX-License-Identifier: GPL-3.0-only

Description
===========

The :man:`cachefilesd(8)` daemon manages the cache data store that is used by
network filesystems such a AFS/CEPH/CIFS/NFS/9P  to cache data locally on disk.

The only prerequisite is that the filesystem that is used to store data
(by default, under :file:`/var/cache/fscache/` must be mounted with
extended user attribute support (``user_xattr``) enabled.

The daemon monitors the disk usage for the cache and automatically removes
files if/when necessary in order to make sure that the cache does not fill
up the disk.

The :ref:`debops.cachefilesd` Ansible role can be used to generate and update
configuration for :command:`cachefilesd` and is mostly useful as a dependency
for other Ansible roles.
