.. Copyright (C) 2022 David Härdeman <david@hardeman.nu>
.. Copyright (C) 2022 DebOps <https://debops.org/>
.. SPDX-License-Identifier: GPL-3.0-only

.. _snappymail__ref_backup_restore:

Backup and restore procedures
=============================

Here you can find information about the backup procedure for the SQLite user
preference/address book database configured by the :ref:`debops.snappymail`
Ansible role as well as tips about restoring the backed-up data.


Backup snapshots
----------------

The :ref:`debops.snappymail` role installs the
:command:`debops-snappymail-sqlite-snapshot` shell script that can be used to
create periodic snapshots of the SQLite databases used by default by SnappyMail
(in case a different database type has been configured via
:envvar:`snappymail__database` and :envvar:`snappymail__database_map`, the
script will not be executed periodically).

By default, three :command:`cron` jobs will be configured by the role to create
daily (7 days), weekly (4-5 weeks) and monthly (12 months) snapshots.  This can
be controlled using the :envvar:`snappymail__snapshot_deploy_state` and
:envvar:`snappymail__snapshot_cron_jobs` default variables. Alternatively, the
periodic :command:`cron` jobs can be disabled, and the
:command:`debops-snappymail-sqlite-snapshot` script can be executed as ``root``
to create a current snapshot of the SnappyMail SQLite database; previous
snapshots are automatically removed in this case with assumption that they have
been transferred to a remote storage by other means.

The :command:`debops-snappymail-sqlite-snapshot` script will acquire database
locks to ensure that the SQLite database is in a consistent state, then
generate a backup copy of the datbase before releasing the lock again. In case
obtaining the lock times out (cf. :envvar:`snappymail__snapshot_timeout`), that
is probably a sign that it is time to move to a full-blown database solution.

The snapshots are stored in the :file:`/var/backups/snappymail/` directory as
compressed tarballs. After finishing the snapshot, the
:command:`debops-snappymail-sqlite-snapshot` script will change ownership of
the created tarballs to the ``backup:backup`` UNIX account and group. This
account can then encrypt the tarballs via its own set of scripts, using GnuPG
assymetric encryption, to prepare them to be sent to a remote location (this
functionality is not implemented by the :ref:`debops.snappymail` role). The
:command:`debops-snappymail-sqlite-snapshot` script will automatically remove
periodic :file:`*.gz.asc` or :file:`*.gz.gpg` files before creating new
iterations to preserve disk space.


Restore procedure
-----------------

The approach described here assumes that a replacement host has been configured
using the :ref:`debops.snappymail` role.

tl;dr version
~~~~~~~~~~~~~

Set up a new SnappyMail host, then copy over the SnappyMail SQLite database
snapshot, replace any existing database, and make sure that all permissions
are correct.

.. code-block:: console

   scp snappymail_week5.sqlite.gz snappymail-host:
   ssh snappymail-host

   gunzip snappymail_week5.sqlite.gz
   chmod 0600 snappymail_week5.sqlite
   sudo chown snappymail:snappymail snappymail_week5.sqlite
   sudo systemctl stop nginx.service
   sudo mv /home/user/snappymail_week5.sqlite /srv/www/sites/snappymail/data/_data_/_default_/AddressBook.sqlite
   sudo systemctl start nginx.service
