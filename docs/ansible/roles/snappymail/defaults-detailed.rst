.. Copyright (C) 2022 David Härdeman <david@hardeman.nu>
.. Copyright (C) 2022 DebOps <https://debops.org/>
.. SPDX-License-Identifier: GPL-3.0-only

Default variable details
========================

Some of the ``debops.snappymail`` default variables have more extensive
configuration than simple strings or lists. Here you can find documentation and
examples for them.

.. only:: html

   .. contents::
      :local:
      :depth: 1

.. _snappymail__ref_configuration:

snappymail__configuration
-------------------------

The ``snappymail__*_configuration`` variables define the contents of the
:file:`data/_data_/_default_/configs/application.ini`
configuration file located in the SnappyMail installation directory. The
contents are defined using YAML data structures, following the
:ref:`universal_configuration` principles, and converted to an ``.ini`` style
file via the role template.

The toplevel items are ``section`` (which correspond to ``.ini`` style
sections, written to the configuration file as ``[section]``), and each
``section`` can define an ``option`` key with a number of key-value
options belonging to the ``section``.

Examples
~~~~~~~~

Override a couple of defailt configuration options:

.. code-block:: yaml

   snappymail__configuration:

     - section: 'webmail'
       options:

         - name: 'allow_themes'
           value: 'Off'

         - name: 'language'
           value: 'de'

         - name: 'language_admin'
           value: 'de'

         - name: 'messages_per_page'
           value: '300'

         - name: 'message_read_delay'
           value: '1'

You can see more examples in the :envvar:`snappymail__default_configuration`
variable.

Syntax
~~~~~~

The configuration options can be defined using a simple or expanded syntax.
Simple syntax uses YAML dictionary keys as the configuration option names (the
``name`` equivalent), and dictionary values as the option values (the ``value``
equivalent). In this case, only one YAML dictionary key/value pair should be
defined at a time.

The expanded definition is enabled when a given configuration entry contains
the ``name`` parameter and uses a set of parameters for better control over
the final output:

``section``
  Required. The name of the ``.ini`` style section to add to the configuration
  file.

``state``
  Optional. If not specified or ``present``, a given option will be
  present in the configuration file. If ``absent``, a given option will be
  removed from the configuration file (or not included if not present).
  If ``init``, the configuration option will be prepared, but will not be
  active and won't show up on the generated configuration file - this can be
  used to prepare configuration that will be activated conditionally in another
  configuration entry. If ``ignore``, a given configuration entry will not be
  evaluated during role execution. If ``comment``, a given configuration option
  will be present in the generated file, but commented out.

``comment``
  Optional. String or YAML text block with comments about a given configuration
  option.

``weight``
  Optional. Positive or negative number which defines the additional "weight"
  of an option. Smaller or negative weight will move the option higher in the
  configuration file, Bigger weight will move the configuration option lower in
  the configuration file.

``options``
  Optional (though defining a ``section`` with no ``options`` makes little
  sense). A list of YAML dictionaries defining the options for a given
  ``section``. Valid parameters include:

  ``name``
    Required. Configuration option name. Configuration entries with the
    same ``name`` parameter are merged in order of appearance; this can be used
    to change configuration options conditionally.

    If the ``option`` parameter is specified, the ``name`` parameter is not
    used as the configuration option name.

  ``option``
    Optional. A string defining the name of the configuration option, which
    will be used in the configuration file instead of the ``name``.

  ``value``
    Required. The value to use in the configuration option. How the value will
    be interpreted depends on the ``type`` parameter (default: string).

  ``type``
    Optional. The type of the configuration option (``bool``, ``integer`` or
    ``string``). The value will automatically be cast/formatted to match the
    defined type.

  ``state``
    Optional. Same as for the toplevel ``section``.

  ``comment``
    Optional. Same as for the toplevel ``section``.

  ``weight``
    Optional. Same as for the toplevel ``section``.

  ``raw``
    Optional. String or which will be included in the generated configuration
    file "as is". If the ``raw`` parameter is defined, it takes precedence over
    the ``name``, ``option`` and ``value`` parameters.


.. _snappymail__ref_domains:

snappymail__domain_configuration
--------------------------------

The ``snappymail__*_domain_configuration`` variables define the contents of the
:file:`data/_data_/_default_/domains/*` configuration files in the SnappyMail
installation directory. The contents are defined using the same syntax as for
:ref:`snappymail__ref_configuration` above, with some minor differences.

First of all, instead of ``section`` as the toplevel item(s), the toplevel
items are ``name``, which define the filename of the generated ``.ini``
files.

The file names are not arbitrary, but correspond to supported domains, so a
file named ``example.com.ini`` will be used to define the settings for a user
logging in using the email address ``foobar@example.com``.

The special name ``default.ini`` is used as a fallback for any domain which
does not have a domain-specic configuration file.

In addition, domains can be disabled using the list defined in
:envvar:`snappymail__disabled_domains`. Note that the domain name ``*``
in that list corresponds to the ``default.ini`` file.

Finally, the toplevel items support the ``copy_from`` key, which defines
another domain file which will be used as the source of configuration
options instead of explicitly defined options. This is mainly useful when
the same IMAP/SMTP/Sieve server(s) are used to support a number of different
domains and the ``default.ini`` file is disabled.

Examples
~~~~~~~~

See :envvar:`snappymail__default_domain_configuration` for an example.


.. _snappymail__ref_plugins:

snappymail__plugins
-------------------

The ``snappymail__*_plugins`` variables define the contents of the
:file:`data/_data_/_default_/config/<plugin>.ini` configuration files in the
SnappyMail installation directory and also control the installation of the
plugins. The contents are defined using the same syntax as for
:ref:`snappymail__ref_configuration` above, with some minor differences.

First of all, instead of ``section`` as the toplevel item(s), the toplevel
items are ``name``, which define the plugin name (and the filename of the
corresponding ``.ini`` files).

The defined plugins will be checked against the plugin manifest downloaded
from the SnappyMail website, and the latest version of the given plugin
will automatically installed (this is because: old plugins are generally not
available from the website; and plugins are usually backwards-compatible).

A current list of available plugins is available from the admin page of
SnappyMail, and the valid configuration options for a given plugin can be
obtained by installing a given plugin and consulting the configuration
file generated for the plugin
(:file:`data/_data_/_default_/config/<plugin>.ini`).

The options defined for a given toplevel ``name`` will implicitly be
put in the ``[plugin]`` section of the generated ``.ini`` file, as expected
by the SnappyMail application.

Examples
~~~~~~~~

See :envvar:`snappymail__default_plugins` for an example.
