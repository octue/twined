.. _schema:

======
Schema
======

This is the core of **twined**, whose whole purpose is to provide and use schemas for digital twins..

.. _requirements:
Requirements of digital twin schema
===================================

A *schema* defines a digital twin, and has multiple roles. It:

#. defines what data is required by a digital twin, in order to run
#. defines what data will be returned by the twin following a successful run
#. defines the formats of these data, in such a way that incoming data can be validated

If this weren't enough, the schema:

#. Must be trustable (i.e. a schema from an untrusted, corrupt or malicious third party should be safe to at least read)
#. Must be machine-readable
#. Must be human-readable
#. Must be searchable/indexable

Fortunately for digital twin developers, many of these requirements have already been seen for data interchange formats
developed for the web. **twined** uses `JSON` and `JSONSchema` to interchange data between digital twins. If you're not
already familiar with JSONSchema (or wish to know why **twined** uses `JSON` over the seemingly more appropriate `XML`
standard), see :ref:`introducing_json_schema`.


.. _specifying_a_framework:
Specifying a framework
======================

We cannot simply expect many developers to create digital twins with a `JSONSchema` then to be able to connect them all
together. **twined** makes things slightly more specific


.. toctree::
   :maxdepth: 0
   :hidden:

   schema_introducing_json

