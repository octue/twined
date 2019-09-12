.. _schema:

======
Schema
======

This is the core of **twined**.

A *schema* defines a digital twin, and has multiple roles. It:

#. defines what data is required by a digital twin, in order to run
#. defines what data will be returned by the twin following a successful run
#. defines the formats of these data, in such a way that incoming data can be validated

If this weren't enough, the schema:

#. Must be trustable (i.e. a schema from an untrusted, corrupt or malicious third party should be safe to at least read)
#. Must be machine-readable
#. Must be human-readable
#. Must be searchable/indexable


.. _schema_json:
Using JSON Schema
=================

Fortunately for digital twin developers, many of these

.. tabs::

   .. code-tab:: py

        import numpy as np
        import es

        def main():
            pass


.. _why_not_xml:
Why not XML
-----------

In a truly `excellent three-part blog<https://www.toptal.com/web/json-vs-xml-part-3>`_


.. toctree::
   :maxdepth: 0
   :hidden:

   turbulence_coherent_structures
   turbulence_wind
   turbulence_tidal
