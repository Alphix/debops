.. Copyright (C) 2023 David Härdeman <david@hardeman.nu>
.. Copyright (C) 2023 DebOps <https://debops.org/>
.. SPDX-License-Identifier: GPL-3.0-only

Default variable details
========================

Some of the ``debops.gssproxy`` default variables have more extensive
configuration than simple strings or lists, here you can find documentation and
examples for them.

.. only:: html

   .. contents::
      :local:
      :depth: 1


.. _gssproxy__ref_configuration:

gssproxy__configuration
-----------------------

The ``gssproxy__*_configuration`` default variables define the configuration of
the :command:`gssproxy` daemon. You can find more details about
:command:`gssproxy` configuration in the :man:`gssproxy(8)` and
:man:`gssproxy.conf(5)` man pages. More detailed per-application examples
are also available from the `upstream git repo`__.

.. __: https://github.com/gssapi/gssproxy/tree/main/docs

The generated configuration files will be located in the
:file:`/etc/gssproxy` directory.

Examples
~~~~~~~~

You can check the :envvar:`gssproxy__default_configuration` variable for the
default (very basic) contents of the main configuration file.

As another example, assume you have a :ref:`debops.nginx` web server which
needs to access files on a Kerberized NFS share, your configuration might look
like this (example based on the `upstream example`__):

.. __: https://github.com/gssapi/gssproxy/blob/main/docs/NFS.md

.. code-block:: yaml

   gssproxy__configuration:

     - name: '40-nginx-nfs'
       comment: 'NFS access for the nginx server'
       options:

         - name: 'service/nginx'
           options:

             - name: 'mechs'
               value: 'krb5'

             - name: 'socket'
               value: '/run/gssproxy.sock'

             - name: 'cred_store_ccache'
               option: 'cred_store'
               value: 'ccache:FILE:/var/lib/gssproxy/clients/krb5cc_nginx'

             - name: 'cred_store_keytab'
               option: 'cred_store'
               value: 'client_keytab:/var/lib/gssproxy/clients/httpd.keytab'

             - name: 'cred_usage'
               value: 'initiate'

             - name: 'euid'
               value: 'www-data'

This will generate a configuration file at
:file:`/etc/gssproxy/40-nginx-nfs.conf` and assumes that a suitable Kerberos
principal has already been created and stored in a keytab at
:file:`/var/lib/gssproxy/clients/httpd.keytab`. The configuration of Kerberos
and creation of principals/keytabs is outside the scope of this role.

Syntax
~~~~~~

The role uses the :ref:`universal_configuration` system to configure the
:command:`gssproxy` daemon. Each configuration entry in the list is
a YAML dictionary. The simple form of the configuration uses the dictionary
keys as the parameter names, and dictionary values as the parameter values.

The top-level dictionaries define the files which should be managed in the
:file:`/etc/gssproxy` directory. These files either have to be named
``gssproxy`` (the main configuration file, see
:envvar:`gssproxy__default_configuration`) or ``XX-<something>`` (where ``XX``
is a number). The ``.conf`` extension will automatically be added by the role.

The second-level dictionaries (defined in the ``options`` key in the top-level
dictionaries) define the ini-style sections in the generated configuration
file.

The third-level dictionaries (defined in the ``options`` key in the
second-level dictionaries) define the configuration options for the given
section.

Each of the three levels of dictionaries define the following parameters:

``name``
  Required. Specifies the name of the :command:`gssproxy` configuration file,
  section or configuration parameter.

  Multiple configuration entries with the same ``name`` parameter are merged
  together in order of appearance. This can be used to modify parameters
  conditionally.

``option``
  Optional, string. If defined, the name to use for a given configuration
  parameter (in third-level dictionaries). This can be used to provide
  several parameters with the same name while avoiding the merging that would
  occur when using the same ``name`` parameter.

``options``
  Optional. List of YAML dicts, used for first- and second-level dicts to
  define the sections and parameters, respectively, which belong to the given
  file/section.

``value``
  Required for configuration options. The value of a given configuration option.
  It can be a string, number, ``True``/``False`` boolean or an empty string.

``comment``
  Optional. A string with a comment which will be included in the generated
  configuration file.

``state``
  Optional. If not specified or ``present``, a given configuration
  file/section/parameter will be present in the generated configuration file.
  If ``absent``, a given file/section/parameter will be removed, if ``comment``
  the given section/parameter will be present but commented out (no effect on
  files).

  If the state is ``init``, the section/parameter will be "primed" in the
  configuration pipeline, but it will be commented out in the generated
  configuration file.

  If the state is ``ignore``, a given configuration entry will not be evaluated
  during role execution. This can be used to activate configuration entries
  conditionally.
