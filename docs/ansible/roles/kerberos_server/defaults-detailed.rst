.. Copyright (C) 2022 David Härdeman <david@hardeman.nu>
.. Copyright (C) 2022 DebOps <https://debops.org/>
.. SPDX-License-Identifier: GPL-3.0-only

Default variable details
========================

Some of the ``debops.kerberos_server`` default variables have more extensive
configuration than simple strings or lists, here you can find documentation and
examples for them.


.. _kerberos_server__ref_realms:

kerberos_server__realms
-----------------------

The ``kerberos_server__*_realms`` variables define the realms which are to be
managed by a given host. The variables are merged in the order defined by the
:envvar:`kerberos_server__combined_realms` variable, which allows modification
of the default configuration through the Ansible inventory.

Examples
~~~~~~~~

See the :envvar:`kerberos_server__default_realms` variable for an example of
existing configuration.

To configure an additional realm, copy the YAML block from
:envvar:`kerberos_server__default_realms` and replace references to the default
realm (``ansible_domain | upper``, e.g. ``EXAMPLE.COM``) with references to the
additional realm (in the example, ``DEV.EXAMPLE.COM``):

.. code-block:: yaml

  kerberos_server__realms:

    - realm: 'DEV.EXAMPLE.COM'
      subtrees: [ '{{ ansible_local.ldap.basedn | d("") }}' ]
      sscope: 'SUB'
      admin_instance: 'admin'
      tasks:

        - name: 'Create default password policy'
          comment: 'Meant to match the slapd ppolicy rules as closely as possible'
          command: 'add_policy
            -history 5
            -minlength 10
            -maxfailure 5
            -failurecountinterval 0
            -lockoutduration 300
            -minclasses 3
            default'

        - name: 'Create randkey password policy'
          comment: 'Randkeys are excluded from length/class checks, this is meant to exclude other keys'
          command: 'add_policy
            -minlength 256
            -maxfailure 1
            -failurecountinterval 0
            -lockoutduration 3600
            -minclasses 5
            randkey'

      ldap_tasks:

        - name: 'Add Kerberos kadmind to realm DEV.EXAMPLE.COM'
          dn: '{{ [ "cn=DEV.EXAMPLE.COM", kerberos_server__ldap_realms_dn ] | join(",") }}'
          attributes:
            krbAdmServers: [ '{{ kerberos_server__ldap_kadmind_binddn }}' ]
          state: '{{ "present" if kerberos_server__primary|d(False)|bool else "ignore" }}'

        - name: 'Add Kerberos KDC to realm DEV.EXAMPLE.COM'
          dn: '{{ [ "cn=DEV.EXAMPLE.COM", kerberos_server__ldap_realms_dn ] | join(",") }}'
          attributes:
            krbKdcServers: [ '{{ kerberos_server__ldap_kdc_binddn }}' ]


Syntax
~~~~~~

The variables contain a list of YAML dictionaries, following the
:ref:`universal_configuration` principles. Each dictionary can have the
following parameters:

``realm``
  Required. Name of the realm to create. The convention is that Kerberos realms
  are written in uppercase, resembling domain names.

``subtrees``
  Required. A list of the `base DN(s)` which will be expected to contain
  Kerberos principals in the LDAP DIT. When principals are created, they will
  typically be added to existing LDAP entries (e.g.
  ``uid=someuser,ou=People,dc=example,dc=com``) by adding the
  ``krbPrincipalAux`` and ``krbTicketPolicyAux`` objectClasses to the entry.
  Alternatively, the principal will be created in in the container entry for
  the given realm (e.g.  under
  ``cn=EXAMPLE.COM,cn=Kerberos,ou=Services,dc=example,dc=com``) and a link
  attribute (``krbObjectReferences``) will be set that points to the LDAP entry
  which the principal belongs to. See :ref:`kerberos_server__ref_ldap_dit` for
  more details. Both the subtrees where principals are stored and where entries
  pointed to by principals are stored need to be covered.

``sscope``
  Required. The scope of the search which will be done below the `base DN(s)`
  defined in ``subtrees`` above. Can be either ``1`` (one level), ``2``
  (two levels) or ``SUB`` (any number of sublevels).

``admin_instance``
  Required. The instance name for principals which are considered to be
  Kerberos administrators. These principals (e.g.
  ``someuser/admin@EXAMPLE.COM``) can use the :command:`kadmin` command
  to create/delete/modify other principals. The conventional instance
  to use is ``admin``.

``tasks``
  Optional. A YAML dictionary with the following entries:

  ``name``
    Required. The ``name`` provides a user-readable description of what the
    ``command`` is meant to achieve.

  ``command``
    Required. Must be written as a :command:`kadmin` command (see
    :man:`kadmin(8)`).

  ``state``
    Optional. Same as for ``state`` below.

``ldap_tasks``
  Optional. A YAML dictionary with LDAP tasks to be carried out after a
  realm has been created/configured. Check the :ref:`ldap__ref_tasks` and
  :ref:`kerberos_server__ref_ldap_access` documentation for further details.

``state``
  Optional. If not specified or ``present``, the realm will be
  created/configured. If ``absent``, ``init`` or ``ignore``, the realm will
  not be configured/created, but any old realm configuration will be retained.

``weight``
  Optional. A positive or negative number which can be used to affect the order
  of realms to be generated. Positive numbers add more "weight" to the realm
  making it appear "lower" in the list; negative numbers substract the "weight"
  and therefore move the realm up in the list.


.. _kerberos_server__ref_stash:

Stash Files
-----------

When a new realm is created (using the :man:`kdb5_ldap_util(8)` tool), a random
`master database password` is generated and stored in a special `keytab` file,
known as a `stash` file. This file is used by the :command:`krb5kdc` and
:command:`kadmind` daemons to access the Kerberos realm data.

The stash file will be stored on each Kerberos server (in the location defined
by :envvar:`kerberos_server__remote_stash_path_base`, plus the name of the
realm, e.g. in :file:`/etc/krb5kdc/.k5.EXAMPLE.COM`) and also locally on the
Ansible controller (typically in :file:`secret/kerberos/stash.EXAMPLE.COM`, see
:envvar:`kerberos_server__local_stash_path_base`).

While the Kerberos data stored in the LDAP DIT will be backed up as part of
the LDAP DIT backup configured by the :ref:`debops.slapd` role, you also need
the stash file stored on the Ansible controller in order to use this backup
in case you need to reinstall the Kerberos environment. If the `stash` file
is missing on a target host, but present on the Ansible controller, it will be
copied to the host. If the file is missing on the controller, the realm will
be recreated and the new `stash` file will be stored on the controller.
