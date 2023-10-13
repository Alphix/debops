.. Copyright (C) 2023 David Härdeman <david@hardeman.nu>
.. Copyright (C) 2023 DebOps <https://debops.org/>
.. SPDX-License-Identifier: GPL-3.0-only

Default variable details
========================

Some of the ``debops.cachefilesd`` default variables have more extensive
configuration than simple strings or lists, here you can find documentation and
examples for them.

.. only:: html

   .. contents::
      :local:
      :depth: 1


.. _cachefilesd__ref_configuration:

cachefilesd__configuration
--------------------------

The ``cachefilesd__*_configuration`` default variables define the configuration
of the :command:`cachefilesd` daemon. You can find more details about
:command:`cachefilesd` configuration in the :man:`cachefilesd(8)` and
:man:`cachefilesd.conf(5)` man pages.

The generated configuration files will be located at
:file:`/etc/cachefilesd.conf`.


Examples
~~~~~~~~

You can check the :envvar:`cachefilesd__original_configuration` variable for
the default contents of the main configuration file.


Syntax
~~~~~~

The role uses the :ref:`universal_configuration` system to configure the
:command:`cachefilesd` daemon. Each configuration entry in the list is
a YAML dictionary. The simple form of the configuration uses the dictionary
keys as the parameter names, and dictionary values as the parameter values.

If the YAML dictionary contains the ``name`` key, the configuration switches
to the complex definition mode, with configuration options defined by specific
parameters:

``name``
  Required. Specifies the name of the configuration parameter.

  Multiple configuration entries with the same ``name`` parameter are merged
  together in order of appearance. This can be used to modify parameters
  conditionally.

``option``
  Optional, string. If defined, the name to use for a given configuration
  parameter. This can be used to provide several parameters with the same name
  while avoiding the merging that would occur when using the same ``name``
  parameter.

``value``
  Optional, string or number. The value of a given configuration option.

``comment``
  Optional. A string with a comment which will be included in the generated
  configuration file.

``state``
  Optional. If not specified or ``present``, a given configuration
  parameter will be present in the generated configuration file.

  If ``absent``, a given parameter will be removed, if ``comment``
  the given section/parameter will be present but commented out.

  If the state is ``init``, the parameter will be "primed" in the
  configuration pipeline, but it will be commented out in the generated
  configuration file.

  If the state is ``ignore``, a given configuration option will not be
  evaluated during role execution. This can be used to activate configuration
  entries conditionally.
