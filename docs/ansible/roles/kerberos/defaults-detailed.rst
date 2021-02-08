.. Copyright (C) 2022 David Härdeman <david@hardeman.nu>
.. Copyright (C) 2022 DebOps <https://debops.org/>
.. SPDX-License-Identifier: GPL-3.0-only

Default variable details
========================

Some of ``debops.kerberos`` default variables have more extensive configuration
than simple strings or lists, here you can find documentation and examples for
them.

.. only:: html

   .. contents::
      :local:
      :depth: 1

.. _kerberos__ref_tasks:

kerberos__tasks
---------------

The ``kerberos__*_tasks`` variables define a custom set of tasks that will be
executed against the Kerberos database, in the specified order. This requires
the role to be able to access the Kerberos credentials of the Ansible user,
on the Ansible Controller. See the :ref:`kerberos__ref_admin` for more details;
this section describes the syntax of the Kerberos tasks themselves.

.. note:: Remember, these are not "Ansible tasks", they are "Kerberos tasks"
          performed against the Kerberos database itself, via the Ansible
          Controller

Examples
~~~~~~~~

See the :envvar:`kerberos__default_tasks` variable and
:ref:`kerberos__ref_dependency` for examples.

Syntax
~~~~~~

The variables contain a list of YAML dictionaries, each dictionary can have
specific parameters:

``name``
  Required. The name of a given task, displayed during Ansible execution. It's
  an equivalent of the ``name`` keyword in Ansible tasks lists. Its value does
  not affect the actions performed in the Kerberos database.

``principal``
  Required. The full name of the Kerberos principal to create. For example,
  ``someuser@EXAMPLE.ORG``.

``path``
  Optional. The path to the keytab where the principal should be stored or
  removed.

``mode``
  Required if ``path`` is defined. The file permissions of the keytab file.

``owner``
  Required if ``path`` is defined. The owner of the keytab file.

``group``
  Required if ``path`` is defined. The group of the keytab file.

``state``
  Optional. If "present", or undefined, the principal will be created and,
  optionally, stored in the keytab defined by the path parameter. If "ignore",
  no action will be taken. If "absent", the principal will be removed from the
  Kerberos database and, if a path is defined, from the given keytab.

``ldap_dn``
  Optional. If specified, and a new principal is created, it will be stored in
  the LDAP directory as part of the given DN (using a ``krbPrincipalAux``
  object class).


.. _kerberos__ref_configuration:

kerberos__configuration
-----------------------

The ``kerberos__*_configuration`` variables define the contents of the
:file:`/etc/krb5.conf` configuration file which is used by all Kerberos clients
on a given host to find the Kerberos servers and related configuration options.
See :man:`krb5.conf(5)` for details of the supported options.

The ``kerberos__*_configuration`` entries are merged together using
:ref:`universal_configuration`, and the Ansible inventory can be used to
override the defaults provided by the role (see
:envvar:`kerberos__default_configuration`).

Examples
~~~~~~~~

Change the default ticket lifetime (if permitted by the KDC):

.. code-block:: yaml

   kerberos__configuration:

     - section: 'libdefaults'
       options:

         - name: 'ticket_lifetime'
           value: '48h'

Add another realm for use by clients (this will only inform the clients about
the existence of the realm, to actually create realms, see
:ref:`debops.kerberos_server`):

.. code-block:: yaml

   kerberos__configuration:

     - section: 'realms'
       options:

         - name: 'DEV.EXAMPLE.ORG'
           options:

           - name: 'kdc'
             value: 'devkdc1.example.org'

           - name: 'master_kdc'
             value: 'devkdc1.example.org'

           - name: 'kpasswd_server'
             value: 'devkdc1.example.org'

           - name: 'admin_server'
             value: 'devkdc1.example.org'


Syntax
~~~~~~

The variables contain a list of YAML dictionaries, following the
:ref:`universal_configuration` principles. Each dictionary can have the
following parameters:

``section``
  Required. Name of the :man:`krb5.conf(5)` configuration section in which a
  given configuration option should be included. This parameter is used as an
  "anchor", configuration entries with the same ``section`` are combined
  together and affect each other in order of appearance.
  are written in uppercase, resembling domain names.

``state``
  Optional. If not specified or ``present``, a given section will be included
  in the generated configuration file. If ``absent``, the section will not be
  included in the file. If ``ignore``, a given configuration entry will not be
  evaluated during role execution. If ``hidden``, the section's header and title
  will be hidden in the generated configuration file.

``weight``
  Optional. A positive or negative number which can be used to affect the order
  of sections in the generated configuration file. Positive numbers add more
  "weight" to the section making it appear "lower" in the file; negative
  numbers substract the "weight" and therefore move the section upper in the
  file.

``options``
  Required. A list of configuration options for a given section. The ``options``
  parameters from configuration entries with the same ``section`` parameter are
  merged together in order of appearance and can affect each other.

  The options can be specified in a simple form as key/vaule pairs, where the
  key is the option name and value is the option value. Alternatively, if the
  ``name`` and ``value`` parameters are used, the entries can use an extended
  format with specific parameters:

  ``name``
    Required. The name of a given :man:`sssd.conf(5)` configuration option
    for a given ``section``. Options with the same ``section`` and ``name``
    will be merged in order of appearance.

  ``options``
    Either ``options`` or ``value`` is required. This parameter can be used
    recursively to create "subsections", which can in turn contain further
    "subsections", as explained in the :man:`krb5.conf(5)` man page.

  ``value``
    Either ``value`` or ``options`` is required. The value of a given
    configuration option ("tag", to use the wording of the :man:`krb5.conf(5)`
    man page). It can be either a string, a boolean, a number, or a YAML list
    (elements will be joined with commas).

  ``raw``
    Optional. String or YAML text block which will be included in the
    configuration file "as is". If this parameter is specified, the ``name``
    and ``value`` parameters are ignored - you need to specify the
    entire line(s) with configuration option names as well.

  ``state``
    Optional. If not defined or ``present``, a given configuration option or
    section will be included in the generated configuration file. If ``absent``,
    ``ignore`` or ``init``, a given configuration option or section will not be
    included in the generated file. If ``comment``, the option will be included
    but commented out and inactive.

  ``comment``
    Optional. String or YAML text block that contains comments about a given
    configuration option.
