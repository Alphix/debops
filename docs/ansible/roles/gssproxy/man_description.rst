.. Copyright (C) 2023 David Härdeman <david@hardeman.nu>
.. Copyright (C) 2023 DebOps <https://debops.org/>
.. SPDX-License-Identifier: GPL-3.0-only

Description
===========

The :man:`gssproxy(8)` daemon is a daemon which manages access to GSSAPI
credentials.

Instead of storing credentials (Kerberos keytabs) on disk and giving
daemons direct access to the long-lived keys contained therein, the
daemon provides a proxy service which allows clients to use the principals
without having access to the underlying keytabs.

This is used by kernel-mode GSS-API applications (CIFS, NFS, AFS, ...) which
need to be able to perform upcalls to a user-level daemon.

The daemon also enables isolation and privilege separation for user-mode
applications. For example: letting HTTP servers use but not see the keytab
entries for HTTP/* principals for accepting security contexts or clients
which need to be able to access NFS shares.

The :ref:`debops.gssproxy` Ansible role can be used to generate and update
configuration for :command:`gssproxy` and is mostly useful as a dependency
for other Ansible roles.
