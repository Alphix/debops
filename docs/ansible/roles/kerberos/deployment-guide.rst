.. Copyright (C) 2022 David Härdeman <david@hardeman.nu>
.. Copyright (C) 2022 DebOps <https://debops.org/>
.. SPDX-License-Identifier: GPL-3.0-only

.. _kerberos__ref_deployment:

Deployment guide
================

.. only:: html

   .. contents::
      :local:


.. _kerberos__ref_host_principals:

Host principals
---------------

By default this role will create a host principal for each host which is
executed against. The host principal (e.g.
``host/somehost.example.org@EXAMPLE.ORG``) will be stored in the corresponding
host LDAP entry created by the :ref:`debops.ldap` role (e.g.
`cn=somehost.example.org=Hosts,dc=example,dc=org`).

The host principal serves two purposes. First, it allows the host to verify
that tickets were issued by a genuine KDC. Second, it allows clients to verify
that they are communicating with the intended host. The host principal serves
essentially the same function as a service principal, except that it relates to
the host as a whole rather than any specific network service. Examples of
services which authenticate using the host principal include ``SSH`` (see
:ref:`debops.sshd`) and the ``root`` account will also, under some
circumstances, (e.g. when accessing NFS mounts without a valid Kerberos
ticket), use the principal.

Hosts can also use the principal to bind to the LDAP server in case there is
not a more appropriate, service-specific account available for that purpose.


.. _kerberos__ref_principal_storage:

Principal storage
-----------------

Traditionally, all principals for the host and various services have been
stored combined in :file:`/etc/krb5.keytab`. This role organizes things a bit
differently.  All principals are created and stored in individual keytabs under
:file:`/etc/krb5.keytab.d`, named according to the primary/service name of the
principal.

For example, a principal like ``nfs/host.example.org@EXAMPLE.ORG`` will be
stored as :file:`/etc/krb5.keytab.d/nfs.keytab` on ``host.example.org``. This
allows for a more fine-grained access control by setting appropriate file
system permissions on the individual keytabs.

For improved compatibility with software which expects :file:`/etc/krb5.keytab`
to be present, it is created as a symlink to
:file:`/etc/krb5.keytab.d/host.keytab`.


.. _kerberos__ref_dependency:

Use as a dependent role
-----------------------

The :ref:`debops.kerberos` role is designed to be used as an API between
Ansible roles and the Kerberos infrastructure. Roles can define a list of
:ref:`Kerberos tasks <kerberos__ref_tasks>` which are passed to the
:ref:`debops.kerberos` role using role dependent variables on the playbook
level. These Keberos tasks will be executed using the
:ref:`kerberos__ref_admin` interface in the LDAP directory.

This API allows the Kerberos integration to be provided in a single, specific
role (:ref:`debops.kerberos`), so that other Ansible roles don't have to
implement different ways of accessing and manipulating Kerberos keytabs by
themselves.

For example, if a service named ``foobar`` needs a principal to be created and
stored in a keytab, it can define a suitable task as a variable (this assumes
that the LDAP entry
``uid=foobar,cn=host.example.org,ou=Hosts,dc=example,dc=org`` has already been
created, e.g. via the :ref:`ldap__ref_dependency`):

.. code-block:: yaml

   foobar__kerberos__dependent_tasks:
     - name: 'Ensure that the Kerberos principal foobar/host.example.org@EXAMPLE.ORG exists'
       principal: 'foobar/host.example.org@EXAMPLE.ORG'
       path: '/etc/krb5.keytab.d/foobar.keytab'
       mode: '0640'
       owner: 'foobar'
       group: 'foobar'
       state: 'present'
       ldap_dn: 'uid=foobar,dc=host.example.org,ou=Hosts,dc=example,dc=org'

This variable can then be used in a playbook by adding:

.. code-block:: yaml

   - role: kerberos
     tags: [ 'role::kerberos', 'skip::kerberos' ]
     kerberos__dependent_tasks:
       - '{{ foobar__kerberos__dependent_tasks }}'

See the :ref:`debops.nfs` role for a real example of Kerberos integration.


.. _kerberos__ref_dns:

Kerberos discovery via DNS
--------------------------

The ``debops.kerberos`` role uses several DNS ``SRV`` (:rfc:`2782`) and ``TXT``
(:rfc:`1464`) records to locate the KDCs and other Kerberos-related services
for the local realm. By default, this information will then be hardcoded in
:file:`/etc/krb5.conf` in order to provide resilience in case of DNS issues and
since not all sites make use of DNSSEC. The records are nevertheless useful for
unconfigured clients and for the initial setup.

The DNS TXT record name is:

- ``_kerberos.<domain>`` - for the realm name (`internet draft`__)

.. __: https://tools.ietf.org/id/draft-vanrein-dnstxt-krb1-09.html

The DNS SRV record service names are:

- ``_kerberos._udp.<domain>`` - for the KDC(s) (:rfc:`4120`)
- ``_kerberos._tcp.<domain>`` - for the KDC(s), if available via TCP (:rfc:`4120`)
- ``_kerberos-master._udp.<domain>`` - for the master KDC
- ``_kerberos-master._tcp.<domain>`` - for the master KDC, if available via TCP
- ``_kpasswd._udp.<domain>`` - for the :man:`kpasswd (1)` service
- ``_kpasswd._tcp.<domain>`` - for the :man:`kpasswd (1)` service, if available via TCP
- ``_kerberos-adm._tcp.<domain>`` - for the :man:`kadmind (8)` service
- ``_kerberos-iv._udp.<domain>`` - for Kerberos v4 KDC(s) (deprecated)

Note that the ``*._tcp.<domain>`` records are only used by some Kerberos
implementations By default, MIT Kerberos KDCs do not listen to the TCP port.
See the `MIT Documentation`__ for more details.

.. __: https://web.mit.edu/kerberos/krb5-latest/doc/admin/realm_config.html#hostnames-for-kdcs

.. note:: The DNS ``SRV`` specification requires the hostnames used as targets
          in ``SRV`` records to be canonical names, and not aliases (i.e. the
          target must point to a hostname with an ``A`` or ``AAAA`` record and
          not to a ``CNAME``). Often it will anyway work to point a ``SRV``
          record to a ``CNAME``, but strictly speaking, it is not RFC compliant
          (see the "Target" definition on page 3 of :rfc:`2782`).

To create the above records in :command:`dnsmasq`, you can use a configuration
like this:

.. code-block:: ini

   txt-record = _kerberos.example.org,"EXAMPLE.ORG"
   srv-host = _kerberos._udp.example.org,foo.example.org,88,1
   srv-host = _kerberos._udp.example.org,bar.example.org,88,2
   srv-host = _kerberos-master._udp.example.org,foo.example.org,88
   srv-host = _kerberos-adm._tcp.example.org,foo.example.org,749
   srv-host = _kpasswd._udp.example.org,foo.example.org,464
   cname = kdc1.example.org,foo.example.org
   cname = kdc2.example.org,bar.example.org
   cname = kerberos.example.org,foo.example.org

.. note:: The ``CNAME`` records only works if :command:`dnsmasq` already "knows"
          the hosts ``foo`` and ``bar`` (e.g. from DHCP or :file:`/etc/hosts`).

If you are using the :ref:`debops.dnsmasq` role, the above configuration can
be set in the Ansible inventory, e.g. something like this:

.. code-block:: yaml

   dnsmasq__dns_records:
     - txt: '_kerberos.example.org'
       value: 'EXAMPLE.ORG'

     - srv: '_kerberos._udp.example.org'
       target: 'foo.example.org'
       port: '88'
       priority: '1'

     - srv: '_kerberos._udp.example.org'
       target: 'bar.example.org'
       port: '88'
       priority: '2'

     - srv: '_kerberos-master._udp.example.org'
       target: 'foo.example.org'
       port: '88'

     - srv: '_kerberos-adm._tcp.example.org'
       target: 'foo.example.org'
       port: '749'

     - srv: '_kpasswd._udp.example.org'
       target: 'foo.example.org'
       port: '464'

   dnsmasq__dhcp_hosts:
     - name: 'foo'
       comment: 'Primary KDC'
       domain: 'example.org'
       mac: '00:00:5e:00:53:04'
       ip: '192.0.2.1'
       cname: [ 'kdc1', 'kerberos' ]

     - name: 'bar'
       comment: 'Secondary KDC'
       domain: 'example.org'
       mac: '00:00:5e:00:53:05'
       ip: '192.0.2.2'
       cname: [ 'kdc2' ]

Or if you are using ISC BIND, the zone file could look like this:

.. code-block:: none

   _kerberos.example.org.	      259200 IN	TXT	"EXAMPLE.ORG"
   _kerberos._udp.example.org.	      259200 IN	SRV	1 0 88 foo.example.org.
   _kerberos._udp.example.org.	      259200 IN	SRV	2 0 88 bar.example.org.
   _kerberos-master._udp.example.org. 259200 IN	SRV	1 0 88 foo.example.org.
   _kerberos-adm._tcp.example.org.    259200 IN	SRV	1 0 749 foo.example.org.
   _kpasswd._udp.example.org.         259200 IN SRV	1 0 464 foo.example.org.
   kdc1.example.org.                  259200 IN CNAME	foo.example.org.
   kdc2.example.org.                  259200 IN CNAME	bar.example.org.
   kerberos.example.org.              259200 IN CNAME	foo.example.org.

The values which are obtained via the DNS queries will control the values of
the following variables in the Ansible inventory:

- :envvar:`kerberos__realm_txt_rr`
- :envvar:`kerberos__kdcs_srv_rr`
- :envvar:`kerberos__master_kdc_srv_rr`
- :envvar:`kerberos__kpasswd_srv_rr`
- :envvar:`kerberos__admin_srv_rr`

Which in turn are used to generate the corresponding variables:

- :envvar:`kerberos__realm`
- :envvar:`kerberos__kdcs`
- :envvar:`kerberos__master_kdc`
- :envvar:`kerberos__kpasswd_server`
- :envvar:`kerberos__admin_server`

If the relevant DNS resource records are not configured, the role will use the
following defaults:

- Realm: ``EXAMPLE.ORG`` (uppercase version of ``ansible_domain``)
- KDC: ``[ kdc.example.org ]``
- Master KDC: ``kdc.example.org`` (first entry in KDC list)
- kpasswd server: ``kdc.example.org`` (master KDC)
- kadmin server: ``kdc.example.org`` (master KDC)

If you do not want to rely on DNS service discovery, you can change the
defaults without using DNS service discovery by either defining the
``kerberos__*_rr`` variables (may be useful if you plan to add DNS records
later), using the same syntax as the Ansible `dig lookup`__. For example:

.. __: https://docs.ansible.com/ansible/latest/collections/community/general/dig_lookup.html

.. code-block:: yaml

   kerberos__kdcs_srv_rr:
     - target: 'foo.example.org'
       port: '88'
       priority: '1'

     - target: 'bar.example.org'
       port: '88'
       priority: '2'

Or, you can override the corresponding ``kerberos__*`` variables directly:

.. code-block:: yaml

   kerberos__realm: 'EXAMPLE.ORG'

   kerberos__kdcs: [ 'foo.example.org', 'bar.example.org' ]
